from flask import Flask, request
from typing import Callable
from daisyfl.server.task_manager import TaskManager
from daisyfl.client.client_api_handler import set_alive

_task_manager: TaskManager = None

app = Flask(__name__)

@app.route("/reconnect", methods=["POST"])
def reconnect():
    js = request.get_json()
    if not js.__contains__("address"):
        js["address"] = None
    if not js.__contains__("sleep_duration"):
        js["sleep_duration"] = None
    global _task_manager
    _task_manager.reconnect_to_parent(js["address"], js["sleep_duration"])
    return js, 200

@app.route("/disconnect_clients", methods=["POST"])
def disconnect_clients():
    js = request.get_json()
    if not js.__contains__("address"):
        js["address"] = None
    if not js.__contains__("sleep_duration"):
        js["sleep_duration"] = None
    global _task_manager
    _task_manager.disconnect_clients(js["address"], js["sleep_duration"])
    return js, 200

@app.route("/receive_task", methods=["POST"])
def receive_task():
    js = request.get_json()
    _task_manager.receive_task(task_config=js)
    return js, 200

@app.route("/shutdown", methods=["POST"])
def shutdown():
    set_alive(False)
    _task_manager.shutdown()
    return {}, 200

def listening(ip: str, port: int, task_manager: TaskManager) -> None:
    global _task_manager
    _task_manager = task_manager
    app.run(host=ip, port=port)

