import json
from flask import request, Response
from ErinaServer.Server import ErinaServer
from Erina.config import update, default
from Erina._config.files import configFile
from ErinaServer.Erina.admin.Stats import returnStats, pastMonthErrors, biggestUsers
from Erina.erina_log import logFile

def makeResponse(responseBody, code, minify=False):
    if minify:
        response = Response(json.dumps(responseBody, ensure_ascii=False, separators=(',', ':')))
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    response.headers["Server"] = "ErinaServer v1.0"
    response.status_code = int(code)
    return response

@ErinaServer.route("/erina/api/admin/logs")
def logs():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    logsResult = []
    logFile.blocking = True
    logLines = logFile.readlines()
    logFile.blocking = False
    for log in logLines:
        log = log.replace("\n", "")
        logsResult.append({float(log.split("    ")[0]): log.split("    ")[1]})
    return makeResponse(logsResult, 200, minify)

@ErinaServer.route("/erina/api/admin/stats")
def stats():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    return makeResponse(returnStats(), 200, minify)

@ErinaServer.route("/erina/api/admin/stats/pastMonthErrors")
def errorsCountForPastMonth():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    return makeResponse(pastMonthErrors(), 200, minify)


@ErinaServer.route("/erina/api/admin/stats/biggestUsers")
def usersCount():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    return makeResponse(biggestUsers(), 200, minify)



@ErinaServer.route("/erina/api/admin/config/get")
def getEndpoint():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    data = configFile.read()
    """
    for element in data:
        data[element].pop("keys", None)
    """
    return makeResponse(data, 200, minify)

@ErinaServer.route("/erina/api/admin/config/update", methods=["POST"])
def updateEndpoint():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    if "path" in request.form and "value" in request.form:
        value = request.form.get("value")
        if ":::" in value:
            value = value.split(":::")
        elif value.lower() in ["true", "false"]:
            value = (True if value.lower() == "true" else False)
        update(request.form.get("path"), value)
        return makeResponse({"message": "success"}, 200, minify)
    else:
        return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["path", "value", "minify"], "optionalArgs": ["minify"]}}, 500, minify)

@ErinaServer.route("/erina/api/admin/config/default", methods=["POST"])
def defaultEndpoint():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    default()
    return makeResponse({"message": "success"}, 200, minify)
