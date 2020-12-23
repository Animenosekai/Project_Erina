import re
import os
import json
import shlex
import signal
import subprocess
from time import sleep
from sys import exc_info
from threading import Thread

from safeIO import TextFile
from flask import request, Response
from filecenter import files_in_dir, extension_from_base

from Erina.erina_log import logFile
from Erina.erina_stats import StatsReset
from Erina._config.files import configFile
from Erina.config import update, default, Hash
from ErinaServer.Erina.auth import authManagement
from ErinaServer.Server import ErinaServer, ErinaRateLimit
from ErinaServer.Erina.auth.apiAuth.authReader import APIAuth
from ErinaServer.Erina.admin.utils import convert_to_float, convert_to_int
from Erina.env_information import erina_version, python_executable_path, erina_dir
from ErinaServer.Erina.admin.Stats import returnStats, pastMonthErrors, biggestUsers, returnOverviewStats


def makeResponse(token_verification, request_args, data=None, code=None, error=None):
    """
    Shaping the response
    """
    if not token_verification.success:
        if token_verification.expired:
            responseBody = {"success": False, "error": "EXPIRED_TOKEN", "message": str(token_verification), "data": None}
        elif token_verification.no_token:
            responseBody = {"success": False, "error": "NOT_PROVIDED_TOKEN", "message": str(token_verification), "data": None}
        else:
            responseBody = {"success": False, "error": "WRONG_TOKEN", "message": str(token_verification), "data": None}
        code = 401
    else:
        if error is not None:
            responseBody = {"success": False, "error": error, "data": data}
        else:
            responseBody = {"success": True, "data": data}
            code = 200

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


### LOGS
@ErinaServer.route("/erina/api/admin/logs")
def logs():
    """
    Returns the logs
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            logsResult = []
            logFile.blocking = True
            logLines = logFile.readlines()
            logFile.blocking = False
            for log in logLines:
                try:
                    log = log.replace("\n", "")
                    logsResult.append({convert_to_int(log.split("    ")[0]): " ".join(log.split("    ")[1:])})
                except:
                    pass
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=logsResult)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

### STATS
@ErinaServer.route("/erina/api/admin/stats")
def stats():
    """
    Returns the stats
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=returnStats())
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/overview")
def overviewStats():
    """
    Returns the stats for the overview page
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=returnOverviewStats())
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/pastMonthErrors")
def errorsCountForPastMonth():
    """
    Returns the past month errors
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=pastMonthErrors())
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/biggestUsers")
def usersCount():
    """
    Returns a ranking of the users
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=biggestUsers())
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


#### CONFIG
@ErinaServer.route("/erina/api/admin/config")
def getEndpoint():
    """
    Returns the configs
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=configFile.read())
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/config/update", methods=["POST"])
def updateEndpoint():
    """
    Updates the configs
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "path" in request.form and "value" in request.form:
                value = str(request.form.get("value"))
                path = str(request.form.get("path"))
                if value == "null":
                    value = None
                elif path in ["Erina/logsTimeout", "Line/imagesTimeout", "Search/thresholds/erinaSimilarity", "Search/thresholds/tracemoeSimilarity", "Search/thresholds/saucenaoSimilarity", "Search/thresholds/iqdbSimilarity"]:
                    value = convert_to_float(value)
                elif path in ["Server/port"]:
                    value = convert_to_int(value)
                elif path in ["Server/host"]:
                    value = re.sub("[^0-9.]", "", value)
                elif path in ["Erina/consoleLog", "Erina/fileLog", "Erina/stats", "Twitter/run", "Twitter/ignoreRT", "Twitter/monitoring/checkReplies", "Discord/run", "Line/run", "Server/disableConsoleMessages"]:
                    value = (True if value.lower().replace(" ", "") == "true" else False)
                elif path in ["Erina/flags", "Twitter/ignoredUsers", "Twitter/flags", "Twitter/stream/languages", "Twitter/stream/flags", "Twitter/monitoring/accounts", "Discord/flags", "Line/flags"]:
                    value = value.split(":::")
                elif path in ["Hash/algorithm"]:
                    algorithm = value.lower().replace(" ", "").replace("_", "")
                    if algorithm not in ['ahash', 'a', 'averagehash', 'average', 'chash', 'c', 'dhash', 'd', 'phash', 'p', 'perceptual', 'perceptualhash', 'wHash', 'w', 'dhashvertical', 'dvertical', 'dvert', 'verticald', 'verticaldhash', 'phashsimple', 'psimple', 'perceptualsimple', 'simpleperceptual', 'simplep', 'simplephash', 'simpleperceptualhas']:
                        value = Hash.algorithm
                update(path, value)
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"path": path, "value": value})
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_ARGS", data={"authorizedArgs": ["path", "value", "minify"], "optionalArgs": ["minify"]}, code=400)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))




###### API AUTH

@ErinaServer.route("/erina/api/admin/apiAuth")
def getAPIAuths():
    """
    Retrieves all of the API Auths
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            results = []
            for file in files_in_dir(erina_dir + "/ErinaServer/Erina/auth/apiAuth"):
                if extension_from_base(file) == ".erina":
                    results.append(APIAuth(file.replace(".erina", "")).as_dict())
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=results)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/apiAuth/new")
def newAPIAuth():
    """
    Adds a new API auth
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "name" in request.values and "ratelimit" in request.values:
                newKey = authManagement.createAPIKey()
                newAuthFile = TextFile(erina_dir + "/ErinaServer/Erina/auth/apiAuth/" + newKey + ".erina")
                newAuthFile.append("Name: " + str(request.values.get("name")) + "\n")
                newAuthFile.append("Rate Limit: " + str(request.values.get("ratelimit")) + "\n")
                newAuthFile.append("Key: " + newKey + "\n")
                newAuthFile.append("----STATS----\n")
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"name": request.values.get("name"), "rateLimit": convert_to_float(request.values.get("ratelimit")), "key": newKey, "usage": 0})
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_ARGS", data={"authorizedArgs": ["name", "ratelimit", "minify"], "optionalArgs": ["minify"]}, code=400)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/apiAuth/remove")
def removeAPIAuth():
    """
    Removes an API auth
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "key" in request.values:
                TextFile(erina_dir + "/ErinaServer/Erina/auth/apiAuth/" + request.values.get("key") + ".erina").delete()
                return makeResponse(token_verification=tokenVerification, request_args=request.values)
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_ARGS", data={"authorizedArgs": ["key", "minify"], "optionalArgs": ["minify"]}, code=400)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


###### ACTIONS


def _shutdown():
    """
    Sends a SIGTERM signal to the current process
    """
    sleep(2)
    os.kill(os.getpid(), signal.SIGTERM)

@ErinaServer.route("/erina/api/admin/config/default", methods=["POST"])
def defaultEndpoint():
    """
    Reverts the configs to its default value
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            default()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))



@ErinaServer.route("/erina/api/admin/stats/reset", methods=["POST"])
def resetStats():
    """
    Reset the stats
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            StatsReset()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/logs/reset", methods=["POST"])
def resetLogs():
    """
    Resets the logs
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            logFile.write("")
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/shutdown", methods=["POST"])
def shutdownServer():
    """
    Shuts down ErinaServer
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            Thread(target=_shutdown, daemon=True).start()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/restart", methods=["POST"])
def restartServer():
    """
    Restarts ErinaServer
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina").write(authManagement.currentToken)
            newErinaProcess = subprocess.Popen(shlex.split("/bin/sh"), stdin=subprocess.PIPE, start_new_session=True) # Open a shell prompt
            newErinaProcess.stdin.write(str("cd " + erina_dir + "\n").encode("utf-8"))
            newErinaProcess.stdin.flush()
            newErinaProcess.stdin.write(str(python_executable_path + " ErinaLauncher.py\n").encode("utf-8"))
            newErinaProcess.stdin.flush()
            Thread(target=_shutdown, daemon=True).start()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/update", methods=["POST"])
def updateServer():
    """
    Updates and restarts the server
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            #### DO SOMETHING
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/alive")
@ErinaRateLimit(0.1)
def alive():
    """
    Returns an answer if ErinaServer is alive
    """
    return makeResponse({"message": "Yes, I'm alive!", "success": True}, 200, request.args)