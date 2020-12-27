from os.path import isfile
from ErinaParser.utils.anilist_parser import AnilistCache
import json
from flask import Response
from flask import request
from time import time
from sys import exc_info

from ErinaSearch import erinasearch
from ErinaServer.Server import ErinaServer

from ErinaCaches.utils.Errors import CachingError
from ErinaDB.utils.Errors import DatabaseError
from ErinaHash.utils.Errors import HashingError
from ErinaParser.utils.Errors import ParserError
from ErinaSearch.utils.Errors import SearchingError

from ErinaLine.utils import Parser as LineParser
from ErinaTwitter.utils import Parser as TwitterParser
from ErinaDiscord.utils import Parser as DiscordParser

from Erina.erina_stats import api as APIStats
from Erina.erina_stats import StatsAppend

from Erina.config import Server as ServerConfig

from Erina.env_information import erina_version, erina_dir
from ErinaServer.Server import ErinaRateLimit
from ErinaServer.Erina.auth.apiAuth import authReader

apiEndpoint = "/erina/api"

def error(result):
    for errorType in [CachingError, DatabaseError, HashingError, ParserError, SearchingError]:
        if isinstance(result, errorType):
            return True
    return False



def makeResponse(request_args, cooldown=None, data=None, code=None, error=None, error_message=None):
    """
    Shaping the response
    """
    if "responseType" in request.values:
        responseType = request.values.get("responseType").lower()
    else:
        responseType = "json"

    if responseType == "text":
        if error is not None:
            if code == 500:
                responseBody = "Success: False\nError: {error}\nData: {data}\nMessage: An error occured on the server".format(error=str(error), data=str(data))
            else:
                responseBody = "Success: False\nError: {error}\nData: {data}\nMessage: {message}".format(error=str(error), data=str(data), message=str(error_message))
        else:
            responseBody = "Success: True\n\n" + data
            code = 200
        responseBody += "\nCooldown: " + str(cooldown)
    elif responseType == "html":
        if error is not None:
            if code == 500:
                responseBody = "<p>Success: False</p><br/><p>Error: {error}</p><br/><p>Data: {data}</p><br/><p>Message: An error occured on the server</p>".format(error=str(error), data=str(data))
            else:
                responseBody = "<p>Success: False</p><br/><p>Error: {error}</p><br/><p>Data: {data}</p><br/><p>Message: {message}</p>".format(error=str(error), data=str(data), message=str(error_message))
        else:
            responseBody = "<p>Success: True</p><br/><br/><p>" + str(data).replace("\n", "<br/>") + "</p>"
            code = 200
        responseBody += "<br/><p>Cooldown: " + str(cooldown) + "</p>"
    else:
        if error is not None:
            if code == 500:
                responseBody = {"success": False, "error": error, "data": data, "message": "An error occured on the server"}
            else:
                responseBody = {"success": False, "error": error, "data": data, "message": error_message}
        else:
            responseBody = {"success": True, "data": data}
            code = 200
        responseBody["cooldown"] = cooldown


    if "minify" in request_args:
        if str(request_args.get("minify")).replace(" ", "").lower() in ["true", "0", "yes"]:
            response = Response(json.dumps(responseBody, ensure_ascii=False, separators=(',', ':')))
        else:
            response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    else:
        response = Response(json.dumps(responseBody, ensure_ascii=False, indent=4))
    
    response.headers["Server"] = "ErinaServer " + erina_version
    if responseType == "text":
        response.headers["Content-Type"] = "text/plain"
    elif responseType == "html":
        response.headers["Content-Type"] = "text/html"
    else:
        response.headers["Content-Type"] = "application/json"

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.status_code = int(code)
    return response


@ErinaServer.route(apiEndpoint + "/auth", methods=["GET"])
def auth():
    try:
        if ServerConfig.public_api:
            return makeResponse(request_args=request.values, cooldown=None, data={"status": "Public API", "message": "This is a Public API"})
        if "key" not in request.values:
            return makeResponse(request_args=request.values, cooldown=None, code=400, error="NO_KEY", error_message="No key got provided")
        else:
            currentKey = request.values.get("key")
            if not isfile(erina_dir + "/ErinaServer/Erina/auth/apiAuth/" + currentKey + ".erina"):
                return makeResponse(request_args=request.values, cooldown=None, code=401, error="WRONG_KEY", error_message="The given key isn't registered")
            else:
                currentAuth = authReader.APIAuth(currentKey)
                if currentKey in rate_limiting_api_map:
                    rate = time() - rate_limiting_api_map[currentKey]
                    if rate > currentAuth.rate_limit:
                        if "preciseStats" in request.values and str(request.values.get("preciseStats")).replace(" ", "").lower() in ["true", "0", "yes"]:
                            return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": currentAuth.stats, "cooldown": 0})
                        else:
                            return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": len(currentAuth.stats), "cooldown": 0})
                    else:
                        if "preciseStats" in request.values and str(request.values.get("preciseStats")).replace(" ", "").lower() in ["true", "0", "yes"]:
                            return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": currentAuth.stats, "cooldown": currentAuth.rate_limit - rate})
                        else:
                            return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": len(currentAuth.stats), "cooldown": currentAuth.rate_limit - rate})
                else:
                    if "preciseStats" in request.values and str(request.values.get("preciseStats")).replace(" ", "").lower() in ["true", "0", "yes"]:
                        return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": currentAuth.stats, "cooldown": 0})
                    else:
                        return makeResponse(request_args=request.values, cooldown=None, data={"status": "Private API", "message": "This is a valid key", "key": currentAuth.key, "name": currentAuth.name, "rateLimit": currentAuth.rate_limit, "usage": len(currentAuth.stats), "cooldown": 0})
    except:
        return makeResponse(request_args=request.values, cooldown=None, code=500, error=str(exc_info()[0]))

#@ErinaRateLimit(fromIP=True)
rate_limiting_api_map = {}
@ErinaServer.route(apiEndpoint + "/search", methods=["GET"])
def search():
    cooldown = None
    try:
        if not ServerConfig.public_api:
            if "key" not in request.values:
                return makeResponse(request_args=request.values, cooldown=None, code=400, error="NO_KEY", error_message="This API is not public and no key got provided along with the request")
            else:
                currentKey = request.values.get("key")
                if not isfile(erina_dir + "/ErinaServer/Erina/auth/apiAuth/" + currentKey + ".erina"):
                    return makeResponse(request_args=request.values, cooldown=None, code=401, error="WRONG_KEY", error_message="The given key isn't registered")
                else:
                    currentAuth = authReader.APIAuth(currentKey)
                    currentAuth.authFile.append(str(time()))
                    if currentKey in rate_limiting_api_map:
                        rate = time() - rate_limiting_api_map[currentKey]
                        if rate > currentAuth.rate_limit:
                            rate_limiting_api_map[currentKey] = time()
                        else:
                            return makeResponse(request_args=request.values, cooldown=currentAuth.rate_limit - rate, code=429, error="RATE_LIMITED", error_message="You have exceeded your rate limit")
                    else:
                        rate_limiting_api_map[currentKey] = time()
                    cooldown = currentAuth.rate_limit

        if "responseType" in request.values:
            responseType = request.values.get("responseType").lower()
        else:
            responseType = "json"

        if "anilistID" in request.values:
            StatsAppend(APIStats.searchEndpointCall, f"AniListID >>> {str(request.values.get('anilistID'))}")
            result = erinasearch.anilistIDSearch(request.values.get("anilistID"))
            if "format" in request.values:
                if request.values.get("format") == "line":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=LineParser.makeInfoResponse(result))
                elif request.values.get("format") == "discord":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=DiscordParser.makeInfoResponse(result)[2])

        elif "anime" in request.values:
            StatsAppend(APIStats.searchEndpointCall, f"Anime Search >>> {str(request.values.get('anime'))}")
            result = erinasearch.searchAnime(request.values.get("anime"))
            if "format" in request.values:
                if request.values.get("format") == "line":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=LineParser.makeInfoResponse(result))
                elif request.values.get("format") == "discord":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=DiscordParser.makeInfoResponse(result)[2])
                    
        elif "image" in request.values:
            StatsAppend(APIStats.searchEndpointCall, "Image Search")
            result = erinasearch.imageSearch(request.values.get("image"))
            if "format" in request.values:
                if request.values.get("format") == "twitter":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=TwitterParser.makeTweet(result))
                elif request.values.get("format") == "line":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=LineParser.makeImageResponse(result))
                elif request.values.get("format") == "discord":
                    return makeResponse(request_args=request.values, cooldown=cooldown, data=DiscordParser.makeImageResponse(result)[2])
        else:
            return makeResponse(request_args=request.values, cooldown=cooldown, data={"authorizedArgs": ["anilistID", "anime", "image", "minify", "format"], "optionalArgs": ["minify", "format"]}, code=400, error="MISSING_ARG", error_message="An argument is missing from your request")
        
        if not error(result):
            if responseType == "text" or responseType == "html":
                return makeResponse(request_args=request.values, cooldown=cooldown, data=result.as_text())
            else:
                return makeResponse(request_args=request.values, cooldown=cooldown, data=result.as_dict())
        else:
            if result.type == "ANILIST_NOT_FOUND":
                return makeResponse(request_args=request.values, cooldown=cooldown, code=404, data={"error": result.type, "message": result.message, "timestamp": result.timestamp, "formattedTimestamp": result.formatted_timestamp}, error="ANILIST_NOT_FOUND", error_message="AniList could not find your anime")
            return makeResponse(request_args=request.values, cooldown=cooldown, data={"error": result.type, "message": result.message, "timestamp": result.timestamp, "formattedTimestamp": result.formatted_timestamp}, code=500, error=result.type, error_message="An error occured while retrieving the information")
    except:
        return makeResponse(request_args=request.values, cooldown=cooldown, code=500, error=str(exc_info()[0]))