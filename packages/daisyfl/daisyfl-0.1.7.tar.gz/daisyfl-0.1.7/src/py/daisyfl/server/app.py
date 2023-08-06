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
"""Flower server app."""
from logging import INFO, WARN, ERROR
from typing import Optional, Tuple, Dict, Callable, List

from daisyfl.common.logger import log
from daisyfl.common import (
    Type,
    GRPC_MAX_MESSAGE_LENGTH,
)
from daisyfl.proto.transport_pb2_grpc import add_FlowerServiceServicer_to_server
from daisyfl.server.client_manager import ClientManager, SimpleClientManager
from daisyfl.server.grpc_server.flower_service_servicer import FlowerServiceServicer
from daisyfl.server.grpc_server.grpc_server import (
    generic_create_grpc_server,
    start_grpc_server,
)
from daisyfl.server.history import History
from daisyfl.server.server import Server
from daisyfl.server.server_operator_manager import ServerOperatorManager
from daisyfl.server.task_manager import TaskManager
from daisyfl.server.server_api_handler import listening

import threading
import time

DEFAULT_SERVER_ADDRESS = "[::]:8887"

def start_server(  # pylint: disable=too-many-arguments
    *,
    # task manager
    zone: bool = False,
    parent_address: str = "",
    # server
    server_address: str = DEFAULT_SERVER_ADDRESS,
    # api_handler
    api_ip: str = None,
    api_port: int = None,
    # grpc
    grpc_max_message_length: int = GRPC_MAX_MESSAGE_LENGTH,
    certificates: Optional[Tuple[bytes, bytes, bytes]] = None,
) -> None:
    # Initialize server and task manager
    initialized_server, initialized_task_manager = _init_defaults(
        # task manager
        zone=zone,
        parent_address=parent_address,
        # api_handler
        api_ip=api_ip,
        api_port=api_port,
    )
    log(INFO, "Starting Flower server",)

    # Start gRPC server
    grpc_server = start_grpc_server(
        client_manager=initialized_server.get_client_manager(),
        server_address=server_address,
        max_message_length=grpc_max_message_length,
        certificates=certificates,
    )
    log(
        INFO,
        "Flower ECE: gRPC server running , SSL is %s",
        "enabled" if certificates is not None else "disabled",
    )

    # Wait until shutdown    
    with initialized_task_manager._cnd_stop:
        initialized_task_manager._cnd_stop.wait()
    initialized_server.disconnect_all_clients(timeout=None)
    # Stop the gRPC server
    grpc_server.stop(grace=1)
    log(INFO, "Daisy server shutdown")
    exit(0)


def _init_defaults(
    # task manager
    zone: bool,
    parent_address: Optional[str],
    # api_handler
    api_ip: str = None,
    api_port: int = None,
) -> Tuple[Server, TaskManager]:
    # client_manager
    client_manager = SimpleClientManager()       
    # server
    server = Server(client_manager=client_manager)
    # server_operator_manager
    server_operator_manager = ServerOperatorManager(server=server)
    # task_manager
    ## zone or master
    manager_type = Type.ZONE if zone else Type.MASTER
    task_manager = TaskManager(
        server_operator_manager=server_operator_manager,
        manager_type=manager_type,
        parent_address=parent_address,
    )
    # api_handler
    start_api_handler(api_ip=api_ip, api_port=api_port, task_manager=task_manager)
    
    return server, task_manager

# api_handler
def start_api_handler(api_ip: str, api_port: int, task_manager: TaskManager) -> bool:
    if isinstance(api_ip, str) and isinstance(api_port, int):
        listener = threading.Thread(target=listening, args=(api_ip, api_port, task_manager))
        listener.setDaemon(True)
        listener.start()
        time.sleep(1)
        if not listener.is_alive():
            log(
                ERROR,
                "client_api_handler failed",
            )
            exit(1)
    else:
        log(
            ERROR,
            "Please check api_ip is string and api_port is integer.",
        )
        exit(1)
    return True
