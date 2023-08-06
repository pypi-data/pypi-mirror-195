import daisyfl as fl
from daisyfl.common import (
    Task,
    ndarrays_to_parameters,
    parameters_to_ndarrays,
    FIT_SAMPLES,
    METRICS,
    LOSS,
    EVALUATE_SAMPLES,
    TID,
)
import argparse
from daisyfl.client.numpy_client import NumPyClient
from daisyfl.client.grpc_client.connection import reconnect_request

# Define Flower Zone client
class ZoneClient(NumPyClient):
    def __init__(self, task_manager, parent_address, set_zc,):
        self.task_manager = task_manager
        set_zc(task_manager=task_manager, zone_client=self)
        # Start Flower client
        fl.client.start_numpy_client(
            parent_address=parent_address,
            client=self,
            _zone=True,
        )

    def get_parameters(self, tid: str):
        # return ndarrays
        parameters = self.task_manager.get_parameters(tid=tid)
        return parameters_to_ndarrays(parameters) if parameters is not None else None
        

    def fit(self, parameters, config):
        parameters, report =  self.task_manager.receive_task(parameters=ndarrays_to_parameters(parameters) , task_config=config)
        # return (ndarrays, num_examples, metrics)
        return parameters_to_ndarrays(parameters), report.config[FIT_SAMPLES], report.config[METRICS]

    def evaluate(self, parameters, config):
        _, report =  self.task_manager.receive_task(parameters=ndarrays_to_parameters(parameters) , task_config=config)
        # return "loss, num_examples, metrics"
        return report.config[LOSS], report.config[EVALUATE_SAMPLES], report.config[METRICS]

    def shutdown(self):
        self.task_manager.shutdown()
    
    def reconnect(self, address: str = None, sleep: int = None) -> None:
        reconnect_request(address, sleep)
