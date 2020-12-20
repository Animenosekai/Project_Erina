import json
from flask import request
from flask import Response

#import config
from ErinaServer.Server import ErinaServer
from ErinaServer.Erina.auth import authManagement
from Erina.env_information import erina_version

authEndpoint = "/erina/auth"

def makeResponse(responseBody, code, request_args):
    if "minify" in request_args:
        if str(request_args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            response = Response(json.dumps(responseBody, ensure_ascii=False, separators=(',', ':')))
        else:
            response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))    
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    response.headers["Server"] = "ErinaServer " + erina_version
    response.status_code = int(code)
    return response

@ErinaServer.route(authEndpoint + "/login")
def login():
    requestArgs = request.values
    if "password" in requestArgs:
        #if requestArgs.get("password") == config.ErinaAdmin_Password:
        if requestArgs.get("password") == "hey":
            return makeResponse(authManagement.createToken(64), 200, request.args)
        else:
            return makeResponse({"error": "WRONG_PASSWORD", "message": "You've entered the wrong password"}, 400, request.args)
    else:
        return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["password", "minify"], "optionalArgs": ["minify"]}}, 500, request.args)