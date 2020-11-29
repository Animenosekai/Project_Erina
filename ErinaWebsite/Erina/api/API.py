import json
from flask import Response
from flask import request

from ErinaSearch import erinasearch
from ErinaWebsite.Server import ErinaServer

from ErinaCaches.utils.Errors import CachingError
from ErinaDB.utils.Errors import DatabaseError
from ErinaHash.utils.Errors import HashingError
from ErinaParser.utils.Errors import ParserError
from ErinaSearch.utils.Errors import SearchingError

apiEndpoint = "/erina/api"

def error(result):
    for errorType in [CachingError, DatabaseError, HashingError, ParserError, SearchingError]:
        if isinstance(result, errorType):
            return True
    return False

def makeResponse(responseBody, code, minify=False):
    if minify:
        response = Response(json.dumps(responseBody, ensure_ascii=False, separators=(',', ':')))
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    response.headers["Server"] = "ErinaServer v1.0"
    response.status_code = int(code)
    return response

@ErinaServer.route(apiEndpoint + "/search", methods=["GET"])
def search():
    minify = False
    requestArgs = request.values
    if "minify" in requestArgs:
        if str(requestArgs.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            minify = True
    if "anilistID" in requestArgs:
        result = erinasearch.anilistIDSearch(requestArgs.get("anilistID"))
    elif "anime" in requestArgs:
        result = erinasearch.searchAnime(requestArgs.get("anime"))
    elif "image" in requestArgs:
        result = erinasearch.imageSearch(requestArgs.get("image"))
    else:
        return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["anilistID", "anime", "image", "minify"], "optionalArgs": ["minify"]}}, 500, minify)
    
    if not error(result):
        return makeResponse(result.as_dict(), 200, minify)
    else:
        return makeResponse({"error": result.type, "message": result.message, "timestamp": result.formatted_timestamp}, 500, minify)
