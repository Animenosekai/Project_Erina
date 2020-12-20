from flask import Flask, Response
from Erina.config import Server
from time import time
import json
from Erina.env_information import erina_version

if Server.disable_console_messages:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

ErinaServer = Flask(__name__)

rate_limit_map = {}

def ErinaRateLimit(rate=1):
    def decorator(function):
        def decorated(*args, **kwargs):
            if function in rate_limit_map:
                if time() - rate_limit_map[function] > rate:
                    rate_limit_map[function] = time()
                    return function(*args, **kwargs)
                else:
                    response = Response(json.dumps({"success": False, "error": "RATE_LIMITED"}, ensure_ascii=False))
                    response.headers["Server"] = "ErinaServer " + erina_version
                    response.headers["Content-Type"] = "application/json"
                    response.status_code = 429
                    return response
            else:
                rate_limit_map[function] = time()
            return function(*args, **kwargs)
        return decorated
    return decorator