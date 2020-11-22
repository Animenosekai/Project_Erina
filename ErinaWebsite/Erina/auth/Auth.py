import json
from flask import request
from flask import Response

#import config
from ErinaWebsite.Server import ErinaServer
from ErinaWebsite.Erina.auth import authManagement

authEndpoint = "/erina/auth"

def makeResponse(responseBody, code, minify=False):
    if minify:
        response = Response(json.dumps(responseBody, ensure_ascii=False))
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    response.headers["Server"] = "ErinaServer v1.0"
    response.status_code = int(code)
    return response

@ErinaServer.route(authEndpoint + "/login")
def login():
    minify = False
    requestArgs = request.values
    if "minify" in requestArgs:
        if str(requestArgs.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    if "password" in requestArgs:
        #if requestArgs.get("password") == config.ErinaAdmin_Password:
        if requestArgs.get("password") == "hey":
            return makeResponse(authManagement.createToken(64), 200, minify)
        else:
            return makeResponse({"error": "WRONG_PASSWORD", "message": "You've entered the wrong password"}, 400, minify)
    else:
        return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["password", "minify"], "optionalArgs": ["minify"]}}, 500, minify)