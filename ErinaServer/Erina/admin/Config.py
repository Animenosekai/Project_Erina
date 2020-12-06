import json
from flask import request, Response
from ErinaServer.Server import ErinaServer
from Erina.config import update, default
from Erina._config.files import configFile

def makeResponse(responseBody, code, minify=False):
    if minify:
        response = Response(json.dumps(responseBody, ensure_ascii=False, separators=(',', ':')))
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    response.headers["Server"] = "ErinaServer v1.0"
    response.status_code = int(code)
    return response

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


@ErinaServer.route("/erina/api/admin/config/default", methods=["POST"])
def defaultEndpoint():
    minify = False
    if "minify" in request.args:
        if str(request.args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    default()
    return makeResponse({"message": "success"}, 200, minify)
