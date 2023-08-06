from typing import Dict, List, Optional, Tuple, Union, Callable
from queue import Queue
from threading import Timer
from daisyfl.common import (
    Code,
    Task,
    Report,
    CURRENT_ROUND,
    EVALUATE,
    TIMEOUT,
    FIT_SAMPLES,
    EVALUATE_SAMPLES,
    LOSS,
    METRICS,
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
from daisyfl.operator.strategy import Strategy

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


def get_configure_fit(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    client_manager: ClientManager,
    config: Dict,
) -> List[Tuple[ClientProxy, FitIns]]:
    client_instructions = strategy.configure_fit(
        server_round=server_round,
        parameters=parameters,
        client_manager=client_manager,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def get_configure_evaluate(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    client_manager: ClientManager,
    config: Dict,
) -> List[Tuple[ClientProxy, EvaluateIns]]:
    client_instructions = strategy.configure_evaluate(
        server_round=server_round,
        parameters=parameters,
        client_manager=client_manager,
    )
    for i in range(len(client_instructions)):
        client_instructions[i][1].config = config.copy()
    return client_instructions

def aggregate_fit(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, FitRes]],
    failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
) -> Tuple[Optional[Parameters], int, Dict[str, Scalar]]:
    """Aggregate fit results using weighted average."""
    results_for_aggregate = [(
        client, type('',(object,),{
            "parameters": res.parameters,
            "num_examples": res.config[FIT_SAMPLES],
            "metrics": res.config[METRICS],
        })()
    ) for client, res in results]

    # Aggregate training results
    parameters, metrics = strategy.aggregate_fit(server_round, results_for_aggregate, failures)
    # num_examples
    num_examples = int(sum([res.config[FIT_SAMPLES] for _, res in results]) / len(results))
    return parameters, num_examples, metrics

def aggregate_fit_async(
    strategy: Strategy,
    server_round: int,
    parameters: Parameters,
    period: float,
    returns_q: Queue,
) -> Tuple[Optional[Parameters], int, Dict[str, Scalar]]:
    def time_out():
        returns_q.put(True)
    Timer(period, time_out).start()
    results = []
    num_examples = 0
    while True:
        future = next(iter(returns_q.get, None))
        if isinstance(future, bool) and future:
            break 
        results, _ = _handle_future(future, results, [])
        if len(results) > 0:
            client, res = results[0]
            results = []
            """Aggregate fit results using weighted average."""
            result_for_aggregate = [(
                client, type('',(object,),{
                    "parameters": res.parameters,
                    "prime": parameters,
                    "num_examples": res.config[FIT_SAMPLES],
                    "metrics": res.config[METRICS],
                    "config": res.config,
                })())]

            # Aggregate training results
            parameters, _ = strategy.aggregate_fit(server_round, result_for_aggregate, [])
            # num_examples
            num_examples =  num_examples + int(res.config[FIT_SAMPLES])
    return parameters, num_examples, {}

def aggregate_evaluate(
    strategy: Strategy,
    server_round: int,
    results: List[Tuple[ClientProxy, EvaluateRes]],
    failures: List[Union[Tuple[ClientProxy, EvaluateRes], BaseException]],
) -> Tuple[Optional[float], int, Dict[str, Scalar]]:
    """Aggregate evaluation losses using weighted average."""
    results_for_aggregate = [(
        client, type('',(object,),{
            "loss": res.config[LOSS],
            "num_examples": res.config[EVALUATE_SAMPLES],
            "metrics": res.config[METRICS],
        })()
    ) for client, res in results]
    
    # Aggregate the evaluation results
    loss, metrics = strategy.aggregate_evaluate(server_round, results_for_aggregate, failures)
    # num_examples
    num_examples = int(sum([res.config[EVALUATE_SAMPLES] for _, res in results]) / len(results))
    return loss, num_examples, metrics

def generate_fit_report(
    server_round: int,
    samples: int,
    metrics_aggregated: Dict[str, Scalar],
)-> Report:
    # (parameters, num_examples, metrics) -> Parameters, Report
    return Report(config={
        CURRENT_ROUND: server_round,
        FIT_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })

def generate_evaluate_report(
    server_round: int,
    samples: int,
    loss_aggregated: Optional[float],
    metrics_aggregated: Dict[str, Scalar],
) -> Report:
    # (loss, num_examples, metrics) -> Report
    return Report(config={
        CURRENT_ROUND: server_round,
        LOSS: loss_aggregated,
        EVALUATE_SAMPLES: samples,
        METRICS: metrics_aggregated,
    })

def wait_for_fit_sync(
    strategy: Strategy,
    client_num: int,
    returns_q: Queue,
    lock_fn: Callable,
):
    results = []
    failures = []
    while True:
        future = next(iter(returns_q.get, None))
        results, failures = _handle_future(future, results, failures)
        if _has_enough_results(strategy, client_num, len(results), len(failures)):
            lock_fn()
            return results, failures

def wait_for_evaluate_sync(
    strategy: Strategy,
    client_num: int,
    returns_q: Queue,
    lock_fn: Callable,
):
    results = []
    failures = []
    while True:
        future = next(iter(returns_q.get, None))
        results, failures = _handle_future(future, results, failures)
        if _has_enough_results(strategy, client_num, len(results), len(failures)):
            lock_fn()
            return results, failures


def _handle_future(future, results, failures):
    # Check if there was an exception
    failure: Union[Tuple[ClientProxy, EvaluateRes], BaseException] = future.exception()
    if failure is not None:
        failures.append(failure)
        return results, failures
    
    # Successfully received a result from a client
    result: Tuple[ClientProxy, FitRes] = future.result()
    _, res = result

    # Check result status code
    if res.status.code == Code.OK:
        results.append(result)
        return results, failures
    
    # Not successful, client returned a result where the status code is not OK
    failures.append(result)
    return results, failures

def _has_enough_results(
    strategy: Strategy,
    client_num: int,
    results_num: int,
    failure_num: int,
) -> bool:
    # TODO:
    if results_num + failure_num == client_num:
        return  True
    return False

