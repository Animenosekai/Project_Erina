import json
from time import time

from safeIO import TextFile
from flask_compress import Compress
from flask_talisman import Talisman
from flask import Flask, Response, request, send_from_directory, redirect

from Erina.env_information import erina_version, erina_dir

# Init ErinaServer
ErinaServer = Flask(__name__)

# Enable compression for all requests
Compress(ErinaServer)

# Secure ErinaServer
Talisman(ErinaServer, content_security_policy={
    'default-src': [
        '\'self\''
    ],
    'script-src': [
        "unsafe-inline"
    ]
})

# Error handlers
@ErinaServer.errorhandler(404)
def page_not_found(e):
    return send_from_directory(erina_dir + "/ErinaServer/Erina/static/html", "404.html"), 404

@ErinaServer.errorhandler(500)
def server_error(e):
    return send_from_directory(erina_dir + "/ErinaServer/Erina/static/html", "500.html"), 500


####### DECORATORS DEFINING
decorator_index = 0

rate_limit_map = {}
ip_rate_limit_map = {}

def ErinaRateLimit(rate=1, fromIP=False):
    def decorator(function):
        global decorator_index
        def decorated(*args, **kwargs):
            if not fromIP:
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
            else:
                if function in ip_rate_limit_map:
                    def getIP():
                        if request.environ.get('HTTP_X_FORWARDED_FOR') is not None: # if the server uses a proxy
                            x_forwarded_for = str(request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0])
                            try:
                                if x_forwarded_for.replace('.', '').isdigit():
                                    return x_forwarded_for
                                else:
                                    return request.remote_addr
                            except:
                                return request.remote_addr
                        else:
                            return request.remote_addr
                    currentIPAddress = getIP()
                    currentFunctionMap = ip_rate_limit_map[function]
                    if function in currentFunctionMap:
                        if time() - currentFunctionMap[currentIPAddress] > rate:
                            currentFunctionMap[currentIPAddress] = time()
                            return function(*args, **kwargs)
                        else:
                            response = Response(json.dumps({"success": False, "error": "RATE_LIMITED"}, ensure_ascii=False))
                            response.headers["Server"] = "ErinaServer " + erina_version
                            response.headers["Content-Type"] = "application/json"
                            response.status_code = 429
                            return response
                    else:
                        currentFunctionMap[currentIPAddress] = time()
                else:
                    ip_rate_limit_map[function] = {}
            return function(*args, **kwargs)
        decoratedFunction = decorated
        decoratedFunction.__name__ = "ErinaRateLimitedEndpoint_" + str(decorator_index)
        decorator_index += 1
        return decoratedFunction
    return decorator



def ErinaStats(name):
    def decorator(function):
        global decorator_index
        def decorated(*args, **kwargs):
            TextFile(erina_dir + "/Erina/stats/userdefinedStats/" + str(name).replace("/", "_") + ".erinalog").append(str(int(time())) + "\n")
            return function(*args, **kwargs)
        decoratedFunction = decorated
        decoratedFunction.__name__ = "ErinaStatEndpoint_" + str(decorator_index)
        decorator_index += 1
        return decoratedFunction
    return decorator