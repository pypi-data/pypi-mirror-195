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
from queue import Queue
from typing import Dict, List, Optional, Tuple, TypedDict
from daisyfl.operator.strategy import Strategy
from daisyfl.common import (
    Parameters,
    Report,
    Task,
    CURRENT_ROUND,
    TIMEOUT,
)
from .msg import (
    WHO_CREATE_THIS_DEMO,
    TIME,
    STUDENT,
    Time,
    Student,
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


class ServerLogic(BaseServerLogic):
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
        # SAY_HI
        ## Get clients and their respective instructions from strategy
        client_instructions = get_configure_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            parameters=parameters,
            client_manager=self.server.get_client_manager(),
            config=task.config,
        )
        config = task.config
        config = _setup_info(config, "Tsung-Han Chang", "Alice", 18, False)
        config = _transition(config)
        client_instructions = _set_config(config, client_instructions)
        ## Collect `fit` results from all clients participating in this round
        lock_fn = self.server.fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
            returns_q=returns_q,
        )
        results, failures = wait_for_fit_sync(
            strategy=self.strategy,
            client_num=len(client_instructions),
            returns_q=returns_q,
            lock_fn=lock_fn,
        )
        # TRAIN
        config = _transition(config)
        client_instructions = _set_config(config, client_instructions)
        ## Collect `fit` results from all clients participating in this round
        lock_fn = self.server.fit_clients(
            client_instructions=client_instructions,
            max_workers=self.server.get_max_workers(),
            timeout=task.config[TIMEOUT],
            returns_q=returns_q,
        )
        results, failures = wait_for_fit_sync(
            strategy=self.strategy,
            client_num=len(client_instructions),
            returns_q=returns_q,
            lock_fn=lock_fn,
        )
        ## Aggregate training results
        parameters_aggregated, samples, metrics_aggregated  = aggregate_fit(
            strategy=self.strategy,
            server_round=task.config[CURRENT_ROUND],
            results=results,
            failures=failures,
        )
        ## Get report
        report = generate_fit_report(
            server_round=task.config[CURRENT_ROUND],
            samples=samples,
            metrics_aggregated=metrics_aggregated,
        )

        return parameters_aggregated, report


def _setup_info(
    config: TypedDict,
    author: str,
    stu_name: str,
    stu_age: int,
    stu_graduate: bool
) -> TypedDict:
    config[WHO_CREATE_THIS_DEMO] = author
    config[STUDENT] = Student(
        name=stu_name,
        age=stu_age,
        graduate=stu_graduate,
    ).to_dict()
    return config

def _transition(
    config: TypedDict,
) -> TypedDict:
    if config.__contains__(TIME):
        config[TIME] = Time((config[TIME] + 1) % Time.__len__()).value
    else:
        config[TIME] = Time(0).value
    return config

def _set_config(
    config: TypedDict,
    client_instructions,
):
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions
