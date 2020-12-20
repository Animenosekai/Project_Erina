import json
from flask import request
from flask import Response

#import config
from ErinaServer.Server import ErinaServer, ErinaRateLimit
from ErinaServer.Erina.auth import authManagement
from Erina.env_information import erina_version, erina_dir
from safeIO import TextFile

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
    response.headers["Content-Type"] = "application/json"
    response.status_code = int(code)
    return response

@ErinaServer.route(authEndpoint + "/login", methods=["POST"])
@ErinaRateLimit(rate=1)
def login():
    requestArgs = request.values
    if "password" in requestArgs:
        if authManagement.verifyPassword(requestArgs.get("password")):
            return makeResponse({"success": True, "token": authManagement.createToken(64)}, 200, request.args)
        else:
            return makeResponse({"success": False, "error": "WRONG_PASSWORD", "message": "You've entered the wrong password"}, 400, request.args)
    else:
        return makeResponse({"success": False, "error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["password", "minify"], "optionalArgs": ["minify"]}}, 500, request.args)

@ErinaServer.route(authEndpoint + "/logout", methods=["POST"])
@ErinaRateLimit(rate=1)
def logout():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        authManagement.logout()
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False}, 400, request.args)

@ErinaServer.route(authEndpoint + "/set", methods=["POST"])
@ErinaRateLimit(rate=1)
def set():
    requestArgs = request.values
    if "password" in requestArgs and "tempCode" in requestArgs:
        if requestArgs.get("tempCode") == authManagement.tempCode:
            authManagement.setPassword(requestArgs.get("password"))
            authManagement.tempCode = None
            return makeResponse({"success": True, "token": authManagement.createToken(64)}, 200, request.args)
        else:
            return makeResponse({"success": False, "error": "wrong", "message": "You've entered the wrong tempCode"}, 400, request.args)
    else:
        return makeResponse({"success": False, "error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["password", "minify"], "optionalArgs": ["minify"]}}, 500, request.args)

@ErinaServer.route(authEndpoint + "/status")
@ErinaRateLimit(rate=1)
def status():
    if TextFile(erina_dir + "/ErinaServer/Erina/auth/password.erina").read().replace(" ", "") == "":
        return makeResponse({"notset": True}, 200, request.args)
    else:
        return makeResponse({"notset": False}, 200, request.args)

@ErinaServer.route(authEndpoint + "/verify")
def verification():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        return "Valid"
    else:
        return "ErinaAdminLoginRedirect"

@ErinaServer.route(authEndpoint + "/displayCode")
@ErinaRateLimit(rate=1)
def displayCode():
    print("[ErinaAdmin] Your temp code is: " + authManagement.createTempCode())
    return makeResponse({"message": "Check your console"}, 200, request.args)