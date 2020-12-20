import json
from flask import Response
from flask import request

from ErinaSearch import erinasearch
from ErinaServer.Server import ErinaServer

from ErinaCaches.utils.Errors import CachingError
from ErinaDB.utils.Errors import DatabaseError
from ErinaHash.utils.Errors import HashingError
from ErinaParser.utils.Errors import ParserError
from ErinaSearch.utils.Errors import SearchingError

from ErinaLine.utils import Parser as LineParser
from ErinaTwitter.utils import Parser as TwitterParser

from Erina.erina_stats import api as APIStats
from Erina.erina_stats import StatsAppend


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
    response.headers["Content-Type"] = "application/json"
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
        StatsAppend(APIStats.searchEndpointCall, f"AniListID >>> {str(requestArgs.get('anilistID'))}")
        result = erinasearch.anilistIDSearch(requestArgs.get("anilistID"))
        if "format" in requestArgs:
            if requestArgs.get("format") == "line":
                return makeResponse(LineParser.makeInfoResponse(result), 200, minify)
    elif "anime" in requestArgs:
        StatsAppend(APIStats.searchEndpointCall, f"Anime Search >>> {str(requestArgs.get('anime'))}")
        result = erinasearch.searchAnime(requestArgs.get("anime"))
        if "format" in requestArgs:
            if requestArgs.get("format") == "line":
                return makeResponse(LineParser.makeInfoResponse(result), 200, minify)
    elif "image" in requestArgs:
        StatsAppend(APIStats.searchEndpointCall, "Image Search")
        result = erinasearch.imageSearch(requestArgs.get("image"))
        if "format" in requestArgs:
            if requestArgs.get("format") == "line":
                return makeResponse(LineParser.makeImageResponse(result), 200, minify)
            elif requestArgs.get("format") == "twitter":
                return makeResponse(TwitterParser.makeTweet(result), 200, minify)
    else:
        return makeResponse({"error": "MISSING_ARGS", "message": "An argument is missing", "extra": {"authorizedArgs": ["anilistID", "anime", "image", "minify", "format"], "optionalArgs": ["minify", "format"]}}, 500, minify)
    
    if not error(result):
        return makeResponse(result.as_dict(), 200, minify)
    else:
        if result.type == "ANILIST_NOT_FOUND":
            return makeResponse({"error": result.type, "message": result.message, "timestamp": result.timestamp, "formattedTimestamp": result.formatted_timestamp}, 404, minify)
        return makeResponse({"error": result.type, "message": result.message, "timestamp": result.timestamp, "formattedTimestamp": result.formatted_timestamp}, 500, minify)
