import json
import re
import os
from time import sleep
from threading import Thread
import shlex
import signal
import subprocess
from flask import request, Response
from ErinaServer.Server import ErinaServer, ErinaRateLimit
from Erina.config import update, default
from Erina._config.files import configFile
from ErinaServer.Erina.admin.Stats import returnStats, pastMonthErrors, biggestUsers
from Erina.erina_stats import StatsReset
from Erina.erina_log import logFile
from ErinaServer.Erina.admin.utils import convert_to_float, convert_to_int
from Erina.config import Hash
from Erina.env_information import erina_version, python_executable_path, erina_dir

from ErinaServer.Erina.auth import authManagement
from safeIO import TextFile


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

@ErinaServer.route("/erina/api/admin/logs")
def logs():
    tokenVerification = authManagement.verifyToken(request.values)
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
        return makeResponse({"success": True, "data": logsResult}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/stats")
def stats():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        results = returnStats()
        results["success"] = True
        return makeResponse(results, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/stats/reset", methods=["POST"])
def resetStats():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        StatsReset()
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/stats/pastMonthErrors")
def errorsCountForPastMonth():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        return makeResponse({"success": True, "data": pastMonthErrors()}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)


@ErinaServer.route("/erina/api/admin/stats/biggestUsers")
def usersCount():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        return makeResponse({"success": True, "data": biggestUsers()}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)


@ErinaServer.route("/erina/api/admin/config/get")
def getEndpoint():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        data = configFile.read()
        """
        for element in data:
            data[element].pop("keys", None)
        """
        data["success"] = True
        return makeResponse(data, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/config/update", methods=["POST"])
def updateEndpoint():
    tokenVerification = authManagement.verifyToken(request.values)
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
            return makeResponse({"success": True, "path": path, "value": value}, 200, request.args)
        else:
            return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["path", "value", "minify"], "optionalArgs": ["minify"]}}, 500, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/config/default", methods=["POST"])
def defaultEndpoint():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        default()
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)



@ErinaServer.route("/erina/api/admin/logs/reset", methods=["POST"])
def resetLogs():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        logFile.write("")
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

def _shutdown():
    sleep(2)
    os.kill(os.getpid(), signal.SIGTERM)

@ErinaServer.route("/erina/api/admin/shutdown", methods=["POST"])
def shutdownServer():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        Thread(target=_shutdown, daemon=True).start()
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)
        
@ErinaServer.route("/erina/api/admin/restart", methods=["POST"])
def restartServer():
    tokenVerification = authManagement.verifyToken(request.values)
    if tokenVerification.success:
        TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina").write(authManagement.currentToken)
        newErinaProcess = subprocess.Popen(shlex.split("/bin/sh"), stdin=subprocess.PIPE, start_new_session=True) # Open a shell prompt
        newErinaProcess.stdin.write(str("cd " + erina_dir + "\n").encode("utf-8"))
        newErinaProcess.stdin.flush()
        newErinaProcess.stdin.write(str(python_executable_path + " ErinaLauncher.py\n").encode("utf-8"))
        newErinaProcess.stdin.flush()
        Thread(target=_shutdown, daemon=True).start()
        return makeResponse({"success": True}, 200, request.args)
    else:
        return makeResponse({"success": False, "error": "login"}, 400, request.args)

@ErinaServer.route("/erina/api/admin/alive")
@ErinaRateLimit(0.1)
def alive():
    return makeResponse({"message": "Yes", "success": True}, 200, request.args)