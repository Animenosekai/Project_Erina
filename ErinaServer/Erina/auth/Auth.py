import json
from sys import exc_info

from flask import request
from flask import Response
from safeIO import TextFile

from ErinaServer.Erina.auth import authManagement
from ErinaServer.Server import ErinaServer, ErinaRateLimit
from Erina.env_information import erina_version, erina_dir

authEndpoint = "/erina/auth"

def makeResponse(responseBody, code, request_args):
    """
    Shapes the response
    """
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
def ErinaServer_Endpoint_Auth_login():
    try:
        if "password" in request.values:
            if authManagement.verifyPassword(request.values.get("password")):
                return makeResponse({"success": True, "data": {"token": authManagement.createToken(64)} }, 200, request.values)
            else:
                return makeResponse({"success": False, "error": "WRONG_PASSWORD", "data": None}, 401, request.values)
        else:
            return makeResponse({"success": False, "error": "MISSING_ARGS", "data": {"authorizedArgs": ["password", "minify"], "optionalArgs": ["minify"]} }, 400, request.values)
    except:
        return makeResponse({"success": False, "error": str(exc_info()[0])}, 500, request.values)

@ErinaServer.route(authEndpoint + "/logout", methods=["POST"])
@ErinaRateLimit(rate=1)
def ErinaServer_Endpoint_Auth_logout():
    try:
        tokenVerification = authManagement.verifyToken(request.values)
        if not tokenVerification.success:
            responseBody = None
            if tokenVerification.expired:
                responseBody = {"success": False, "error": "EXPIRED_TOKEN", "message": str(tokenVerification), "data": None}
            elif tokenVerification.no_token:
                responseBody = {"success": False, "error": "NOT_PROVIDED_TOKEN", "message": str(tokenVerification), "data": None}
            else:
                responseBody = {"success": False, "error": "WRONG_TOKEN", "message": str(tokenVerification), "data": None}
            return makeResponse(responseBody, 401, request.values)
        else:
            authManagement.logout()
            return makeResponse({"success": True, "data": None}, 200, request.values)
    except:
        return makeResponse({"success": False, "error": str(exc_info()[0])}, 500, request.values)

@ErinaServer.route(authEndpoint + "/set", methods=["POST"])
@ErinaRateLimit(rate=1)
def ErinaServer_Endpoint_Auth_set():
    try:
        if "password" in request.values and "tempCode" in request.values:
            if request.values.get("tempCode") == authManagement.tempCode:
                authManagement.setPassword(request.values.get("password"))
                authManagement.tempCode = None
                return makeResponse({"success": True, "data": {"token": authManagement.createToken(64)} }, 200, request.values)
            else:
                return makeResponse({"success": False, "error": "WRONG_TEMPCODE", "data": None}, 401, request.values)
        else:
            return makeResponse({"success": False, "error": "MISSING_ARGS", "data": {"authorizedArgs": ["tempCode", "password", "minify"], "optionalArgs": ["minify"]} }, 400, request.values)
    except:
        return makeResponse({"success": False, "error": str(exc_info()[0])}, 500, request.values)


@ErinaServer.route(authEndpoint + "/verify")
@ErinaRateLimit(rate=1)
def ErinaServer_Endpoint_Auth_verify():
    try:
        if TextFile(erina_dir + "/ErinaServer/Erina/auth/password.erina").read().replace(" ", "") == "":
            return makeResponse({"success": False, "error": "NOT_SET_PASSWORD", "message": "Password Is Not Set"}, 400, request.args)
        tokenVerification = authManagement.verifyToken(request.values)
        if not tokenVerification.success:
            responseBody = None
            if tokenVerification.expired:
                responseBody = {"success": False, "error": "EXPIRED_TOKEN", "message": str(tokenVerification)}
            elif tokenVerification.no_token:
                responseBody = {"success": False, "error": "NOT_PROVIDED_TOKEN", "message": str(tokenVerification)}
            else:
                responseBody = {"success": False, "error": "WRONG_TOKEN", "message": str(tokenVerification)}
            return makeResponse(responseBody, 401, request.values)
        else:
            return makeResponse({"success": True}, 200, request.values)
    except:
        return makeResponse({"success": False, "error": str(exc_info()[0])}, 500, request.values)

@ErinaServer.route(authEndpoint + "/displayCode", methods=["POST"])
@ErinaRateLimit(rate=1)
def ErinaServer_Endpoint_Auth_displayCode():
    try:
        print("[ErinaAdmin] Your temp code is: " + authManagement.createTempCode())
        return makeResponse({"success": True, "message": "Check your console"}, 200, request.values)
    except:
        return makeResponse({"success": False, "error": str(exc_info()[0])}, 500, request.values)