"""Gets the returned json data from the sensor"""

import json
from urllib.request import Request, urlopen
import functools
import time
from pathlib import Path
import os

class SensorConnectionFailure(Exception):
    """Thrown when we can't seemingly communicate with the temp sensor"""

def _retry():
    """A retry decorator for request calls"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raised_exc = None
            for _ in range(5):  # NOTE: Trying out 5 attempts in the real world
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    raised_exc = repr(exc)
                    print(raised_exc)
                    time.sleep(60)

            raise SensorConnectionFailure(f"Retry limit hit when attempting request(s). Exception: {raised_exc}")

        return wrapper

    return decorator

@_retry()
def _do_url_req(url: str) -> dict:
    """Returns a dict of data from the remote sensor"""
    req = Request(
        url=url,
        headers={"Content-Type": "application/json"},
        method="GET"
    )

    with urlopen(req) as resp:
        return json.loads(resp.read().decode("UTF-8"))

def get_sensor() -> str:
    """Gets the endpoint info from the config.json file"""
    conf_file = Path(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(conf_file, "r", encoding="UTF-8") as conf:
        endpoint_data = json.load(conf)

    resp_data = _do_url_req(endpoint_data["endpoint"])
    return resp_data.get(endpoint_data["sensor"], None)

def get_sensor_data(sensor_url: str) -> dict:
    """Returns all data from the sensor"""
    return _do_url_req(sensor_url)

def get_sensor_temp(sensor_url: str) -> float:
    """"""
    return get_sensor_data(sensor_url).get("temp", None)
