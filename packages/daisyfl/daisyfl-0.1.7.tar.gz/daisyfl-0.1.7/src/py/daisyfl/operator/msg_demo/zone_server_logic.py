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
from logging import INFO, WARNING
from typing import Dict, List, Optional, Tuple, TypedDict
from queue import Queue
from daisyfl.operator.strategy import Strategy
from daisyfl.common import (
    Parameters,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
)
from .msg import (
    TIME,
    Time,
)
from daisyfl.common.logger import log

from daisyfl.operator.utils import (
    get_configure_fit,
    aggregate_fit,
    generate_fit_report,
    get_configure_evaluate,
    aggregate_evaluate,
    generate_evaluate_report,
    wait_for_fit_sync,
)
from daisyfl.server import Server
from daisyfl.operator.base.server_logic import ServerLogic as BaseServerLogic


class ZoneServerLogic(BaseServerLogic):
    def __init__(self,
        server: Server,
        strategy: Strategy
    ) -> None:
        self.server: Server = server
        self.strategy: Strategy = strategy

    def fit_round(
        self,
        parameters: Parameters,
        task: Task,
        returns_q: Queue,
    ) -> Optional[
        Tuple[Optional[Parameters], Optional[Report]]
    ]:
        """Perform a single round fit."""
        stage = Time(task.config[TIME])
        if stage == Time.SAY_HI:
            return _say_hi(self, parameters, task, returns_q)
        elif stage == Time.TRAIN:
            return _fit(self, parameters, task, returns_q)
        else:
            raise ValueError("Invalid stage received")


def _say_hi(
    server_logic: ZoneServerLogic,
    parameters: Parameters,
    task: Task,
    returns_q: Queue,
) -> Optional[
    Tuple[Optional[Parameters], Optional[Report]]
]:
    ## Get clients and their respective instructions from strategy
    client_instructions = get_configure_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        parameters=parameters,
        client_manager=server_logic.server.get_client_manager(),
        config=task.config,
    )
    ## Collect `fit` results from all clients participating in this round
    lock_fn = server_logic.server.fit_clients(
        client_instructions=client_instructions,
        max_workers=server_logic.server.get_max_workers(),
        timeout=task.config[TIMEOUT],
        returns_q=returns_q,
    )
    results, failures = wait_for_fit_sync(
        strategy=server_logic.strategy,
        client_num=len(client_instructions),
        returns_q=returns_q,
        lock_fn=lock_fn,
    )
    # Get report
    report = generate_fit_report(
        server_round=task.config[CURRENT_ROUND],
        samples=0,
        metrics_aggregated={},
    )
        
    return parameters, report

def _fit(server_logic: ZoneServerLogic, parameters: Parameters, task: Task, returns_q: Queue,):
    """Perform a single round fit."""
    # Get clients and their respective instructions from strategy
    client_instructions = get_configure_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        parameters=parameters,
        client_manager=server_logic.server.get_client_manager(),
        config=task.config,
    )
    # Collect `fit` results from all clients participating in this round
    lock_fn = server_logic.server.fit_clients(
        client_instructions=client_instructions,
        max_workers=server_logic.server.get_max_workers(),
        timeout=task.config[TIMEOUT],
        returns_q=returns_q,
    )
    results, failures = wait_for_fit_sync(
        strategy=server_logic.strategy,
        client_num=len(client_instructions),
        returns_q=returns_q,
        lock_fn=lock_fn,
    )
    # Aggregate training results
    parameters_aggregated, samples, metrics_aggregated  = aggregate_fit(
        strategy=server_logic.strategy,
        server_round=task.config[CURRENT_ROUND],
        results=results,
        failures=failures,
    )
    # Get report
    report = generate_fit_report(
        server_round=task.config[CURRENT_ROUND],
        samples=samples,
        metrics_aggregated=metrics_aggregated,
    )

    return parameters_aggregated, report
