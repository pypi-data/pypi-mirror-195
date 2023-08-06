from flask import Flask, request
from .grpc_client.connection import reconnect_request

alive = True

def get_alive() -> bool:
    global alive
    return alive

def set_alive(keep_going: bool) -> None:
    global alive
    alive = keep_going

app = Flask(__name__)

@app.route("/reconnect", methods=["POST"])
def reconnect():
    js = request.get_json()
    if not js.__contains__("address"):
        js["address"] = None
    if not js.__contains__("sleep_duration"):
        js["sleep_duration"] = None
    reconnect_request(js["address"], js["sleep_duration"])
    return js, 200

@app.route("/shutdown", methods=["POST"])
def shutdown():
    set_alive(False)
    return {}, 200

def listening(ip: str, port: int,) -> None:
    app.run(host=ip, port=port)


