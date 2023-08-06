# Copyright 2020 Adap GmbH. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Flower server."""


import concurrent.futures
import timeit
from threading import Event
from queue import Queue
from logging import DEBUG, INFO
from typing import Dict, List, Optional, Tuple, Union, Callable

from daisyfl.common import (
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
    Code,
    DisconnectRes,
    EvaluateIns,
    EvaluateRes,
    FitIns,
    FitRes,
    Parameters,
    ReconnectIns,
    Scalar,
)
from daisyfl.common.logger import log
from daisyfl.common.typing import GetParametersIns
from daisyfl.server.client_manager import ClientManager
from daisyfl.server.client_proxy import ClientProxy
from daisyfl.server.history import History

FitResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, FitRes]],
    List[Union[Tuple[ClientProxy, FitRes], BaseException]],
]
EvaluateResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, EvaluateRes]],
    List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
]
ReconnectResultsAndFailures = Tuple[
    List[Tuple[ClientProxy, DisconnectRes]],
    List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]],
]
    

class Server:
    """Flower server."""

    def __init__(
        self, *, 
        client_manager: ClientManager,
    ) -> None:
        self._client_manager: ClientManager = client_manager
        self._max_workers: Optional[int] = None

    # set Server attributes
    def set_max_workers(self, max_workers: Optional[int]) -> None:
        """Set the max_workers used by ThreadPoolExecutor."""
        self._max_workers = max_workers

    # get Server attributes
    def get_client_manager(self) -> ClientManager:
        """Return ClientManager."""
        return self._client_manager

    def get_max_workers(self) -> Optional[int]:
        """Return max_workers."""
        return self._max_workers

    # TODO:
    def disconnect_all_clients(self, timeout: Optional[float]) -> None:
        """Send shutdown signal to all clients."""
        all_clients = self.get_client_manager().all()
        clients = [all_clients[k] for k in all_clients.keys()]
        instruction = ReconnectIns(seconds=None)
        client_instructions = [(client_proxy, instruction) for client_proxy in clients]
        _ = _reconnect_clients(
            client_instructions=client_instructions,
            max_workers=self.get_max_workers(),
            timeout=timeout,
        )

    def fit_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, FitIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
    ) -> FitResultsAndFailures:
        return _fit_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
            timeout=timeout,
            returns_q=returns_q,
        )
    
    def evaluate_clients(
        self,
        client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
        max_workers: Optional[int],
        timeout: Optional[float],
        returns_q: Queue,
    ) -> EvaluateResultsAndFailures:
        return _evaluate_clients(
            client_instructions=client_instructions,
            max_workers=max_workers,
            timeout=timeout,
            returns_q=returns_q,
        )


def _reconnect_clients(
    client_instructions: List[Tuple[ClientProxy, ReconnectIns]],
    max_workers: Optional[int],
    timeout: Optional[float],
) -> ReconnectResultsAndFailures:
    """Instruct clients to disconnect and never reconnect."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        submitted_fs = {
            executor.submit(_reconnect_client, client_proxy, ins, timeout)
            for client_proxy, ins in client_instructions
        }
        finished_fs, _ = concurrent.futures.wait(
            fs=submitted_fs,
            timeout=None,  # Handled in the respective communication stack
        )

    # Gather results
    results: List[Tuple[ClientProxy, DisconnectRes]] = []
    failures: List[Union[Tuple[ClientProxy, DisconnectRes], BaseException]] = []
    for future in finished_fs:
        failure = future.exception()
        if failure is not None:
            failures.append(failure)
        else:
            result = future.result()
            results.append(result)
    return results, failures


def _reconnect_client(
    client: ClientProxy,
    reconnect: ReconnectIns,
    timeout: Optional[float],
) -> Tuple[ClientProxy, DisconnectRes]:
    """Instruct client to disconnect and (optionally) reconnect later."""
    disconnect = client.reconnect(
        reconnect,
        timeout=timeout,
    )
    return client, disconnect


def _fit_clients(
    client_instructions: List[Tuple[ClientProxy, FitIns]],
    max_workers: Optional[int],
    timeout: Optional[float],
    returns_q: Queue,
) -> Callable:
    """Refine parameters concurrently on all selected clients."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        submitted_fs = {
            executor.submit(_fit_client, client_proxy, ins, timeout)
            for client_proxy, ins in client_instructions
        }
        
        event = Event()

        for f in submitted_fs:
            f.add_done_callback(_handle_finished_future_after_fit(returns_q=returns_q, event=event))

        return event.set


def _fit_client(
    client: ClientProxy, ins: FitIns, timeout: Optional[float]
) -> Tuple[ClientProxy, FitRes]:
    """Refine parameters on a single client."""
    fit_res = client.fit(ins, timeout=timeout)
    return client, fit_res


def _handle_finished_future_after_fit(
    returns_q: Queue,
    event: Event,
) -> None:
    """Convert finished future into either a result or a failure."""
    def future_callback_fn(future: concurrent.futures.Future):
        # Expired
        if event.is_set():
            return
        returns_q.put(future)
    return future_callback_fn


def _evaluate_clients(
    client_instructions: List[Tuple[ClientProxy, EvaluateIns]],
    max_workers: Optional[int],
    timeout: Optional[float],
    returns_q: Queue,
) -> EvaluateResultsAndFailures:
    """Evaluate parameters concurrently on all selected clients."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        submitted_fs = {
            executor.submit(_evaluate_client, client_proxy, ins, timeout)
            for client_proxy, ins in client_instructions
        }

        event = Event()

        for f in submitted_fs:
            f.add_done_callback(_handle_finished_future_after_evaluate(returns_q=returns_q, event=event))

        return event.set


def _evaluate_client(
    client: ClientProxy,
    ins: EvaluateIns,
    timeout: Optional[float],
) -> Tuple[ClientProxy, EvaluateRes]:
    """Evaluate parameters on a single client."""
    evaluate_res = client.evaluate(ins, timeout=timeout)
    return client, evaluate_res


def _handle_finished_future_after_evaluate(
    returns_q: Queue,
    event: Event,
) -> None:
    """Convert finished future into either a result or a failure."""
    def future_callback_fn(future: concurrent.futures.Future):
        # Expired
        if event.is_set():
            return
        returns_q.put(future)
    return future_callback_fn
