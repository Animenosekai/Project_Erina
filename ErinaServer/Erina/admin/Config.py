"""
Main ErinaConfig endpoints\n
Project Erina
"""

import re
import os
import json
import signal
import platform
import traceback
from io import BytesIO
from time import sleep
from sys import exc_info
from zipfile import ZipFile
from base64 import b64decode
from threading import Thread
from urllib.parse import urlparse
from distutils.dir_util import copy_tree
from shutil import copyfile, make_archive
from threading import active_count as current_threads

import psutil
import requests
from flask import request, Response
from safeIO import JSONFile, TextFile
from flask.helpers import send_from_directory
from ErinaDiscord.erina_discordbot import startDiscord
from filecenter import delete, exists, files_in_dir, extension_from_base, isdir, isfile, make_dir, move


from Erina.erina_log import logFile
from Erina.erina_stats import StatsReset
from Erina._config.files import configFile
from Erina._config.classes import environ
from ErinaServer.Erina.auth import authManagement
from ErinaServer.Server import ErinaServer, ErinaRateLimit
from ErinaLine.erina_linebot import initHandler as initLine
from ErinaTwitter.utils.Stream import ErinaStreamListener
from ErinaServer.Erina.auth.apiAuth.authReader import APIAuth
from ErinaDB.ManamiDB.manami_db_verification import verify_manami_adb
from ErinaDB.ManamiDB.manami_db_data import Database as ManamiDatabase
from Erina.config import update, default, Hash, Twitter, Discord, Line
from ErinaTwitter.erina_twitterbot import latestResponses, ErinaTwitter
from Erina.utils import convert_to_float, convert_to_int, get_scaled_size, convert_to_boolean
from Erina.env_information import erina_version, erina_dir, python_version_info, pid, cpu_count
from ErinaServer.Erina.admin.Stats import returnStats, pastMonthErrors, biggestUsers, returnOverviewStats

class ErinaUpdateError(Exception):
    """
    When an error occurs while updating
    """
    def __init__(self, message):
        super().__init__(message)


def makeResponse(token_verification, request_args, data=None, code=None, error=None, error_message=None):
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
            if code == 500:
                responseBody = {"success": False, "error": error, "data": data, "message": "An error occured on the server"}
            else:
                responseBody = {"success": False, "error": error, "data": data, "message": error_message}
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
def ErinaServer_Endpoint_Admin_Config_logs():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

### STATS
@ErinaServer.route("/erina/api/admin/stats")
def ErinaServer_Endpoint_Admin_Config_stats():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/overview")
def ErinaServer_Endpoint_Admin_Config_overviewStats():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/pastMonthErrors")
def ErinaServer_Endpoint_Admin_Config_errorsCountForPastMonth():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/stats/biggestUsers")
def ErinaServer_Endpoint_Admin_Config_usersCount():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/twitter/latestResponses")
def ErinaServer_Endpoint_Admin_Config_latestResponses():
    """
    Returns the latest tweets responses
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=latestResponses)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

#### CONFIG
@ErinaServer.route("/erina/api/admin/config")
def ErinaServer_Endpoint_Admin_Config_getEndpoint():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/config/update", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_updateEndpoint():
    """
    Updates the configs
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "path" in request.form and "value" in request.form:
                originalValue = str(request.form.get("value"))
                value = str(environ(request.form.get("value")))
                path = str(request.form.get("path"))
                if value == "null":
                    value = None
                elif path in ["Erina/logsTimeout", "Line/imagesTimeout", "Search/thresholds/erinaSimilarity", "Search/thresholds/tracemoeSimilarity", "Search/thresholds/saucenaoSimilarity", "Search/thresholds/iqdbSimilarity", "Caches/anilistExpiration"]:
                    value = convert_to_float(value)
                elif path in ["Server/port"]:
                    value = convert_to_int(value)
                elif path in ["Server/host"]:
                    value = re.sub("[^0-9.]", "", value)
                elif path in ["Erina/consoleLog", "Erina/fileLog", "Erina/stats", "Twitter/run", "Twitter/ignoreRT", "Twitter/monitoring/checkReplies", "Discord/run", "Line/run", "Server/publicAPI", "Twitter/imagePreview", "Twitter/checkMentions", "Twitter/checkDM"]:
                    value = convert_to_boolean(value)
                elif path in ["Erina/flags", "Twitter/ignoredUsers", "Twitter/flags", "Twitter/stream/languages", "Twitter/stream/flags", "Twitter/monitoring/accounts", "Discord/flags", "Line/flags"]:
                    value = value.split(":::")
                elif path in ["Hash/algorithm"]:
                    algorithm = value.lower().replace(" ", "").replace("_", "")
                    if algorithm not in ['ahash', 'a', 'averagehash', 'average', 'chash', 'c', 'dhash', 'd', 'phash', 'p', 'perceptual', 'perceptualhash', 'wHash', 'w', 'dhashvertical', 'dvertical', 'dvert', 'verticald', 'verticaldhash', 'phashsimple', 'psimple', 'perceptualsimple', 'simpleperceptual', 'simplep', 'simplephash', 'simpleperceptualhas']:
                        value = Hash.algorithm
                if path == "Twitter/run" and value == True and not Twitter.run:
                    if Twitter.keys.consumer_key is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Twitter", "key": "Consumer Key"}, code=400)
                    elif Twitter.keys.consumer_secret is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Twitter", "key": "Consumer Secret"}, code=400)
                    elif Twitter.keys.access_token_key is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Twitter", "key": "Access Token Key"}, code=400)
                    elif Twitter.keys.access_token_secret is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Twitter", "key": "Access Token Secret"}, code=400)
                    def startTwitter():
                        ErinaTwitter.init()
                        from ErinaTwitter.utils import Stream
                        Stream.startStream()
                    Thread(target=startTwitter, daemon=True).start()
                elif path == "Twitter/run" and value == False and Twitter.run:
                    from ErinaTwitter.utils import Stream
                    Stream.endStream()
                if path == "Discord/run" and value == True and not Discord.run:
                    if Discord.keys.token is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Discord", "key": "Bot Token"}, code=400)
                    startDiscord()
                elif path == "Discord/run" and value == False and Discord.run:
                    from ErinaDiscord.erina_discordbot import client as discordClient
                    discordClient.close()
                elif path == "Line/run" and value == True:
                    if Line.keys.channel_access_token is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Line", "key": "Channel Access Token"}, code=400)
                    elif Line.keys.channel_secret is None:
                        return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_CRITICAL_KEY", data={"client": "Line", "key": "Channel Secret"}, code=400)
                    if not Line.run:
                        Thread(target=initLine, daemon=True).start()
                if str(value) == environ(originalValue):
                    update(path, originalValue)
                    return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"path": path, "value": originalValue})
                else:
                    update(path, value)
                    return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"path": path, "value": value})
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_ARGS", data={"authorizedArgs": ["path", "value", "minify"], "optionalArgs": ["minify"]}, code=400)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))




###### API AUTH

@ErinaServer.route("/erina/api/admin/apiAuth")
def ErinaServer_Endpoint_Admin_Config_getAPIAuths():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/apiAuth/new", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_newAPIAuth():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/apiAuth/remove", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_removeAPIAuth():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


###### ACTIONS


def _shutdown():
    """
    Sends a SIGTERM signal to the current process
    """
    sleep(2)
    os.kill(os.getpid(), signal.SIGTERM)

def _restart():
    """
    Sends a SIGUSR1 signal to the current process
    """
    sleep(2)
    os.kill(os.getpid(), signal.SIGUSR1)

@ErinaServer.route("/erina/api/admin/config/default", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_defaultEndpoint():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))



@ErinaServer.route("/erina/api/admin/stats/reset", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_resetStats():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/logs/reset", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_resetLogs():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))
    

@ErinaServer.route("/erina/api/admin/caches/clean", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_cleanCaches():
    """
    Cleans the caches
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "anilist" in request.values and convert_to_boolean(request.values.get("anilist", False)) == True:
                for file in files_in_dir(erina_dir + "/ErinaCaches/AniList_Cache"):
                    if extension_from_base(file) == ".erina":
                        TextFile(erina_dir + "/ErinaCaches/AniList_Cache/" + file).delete()
            for file in files_in_dir(erina_dir + "/ErinaCaches/Erina_Cache"):
                if extension_from_base(file) == ".erina":
                    TextFile(erina_dir + "/ErinaCaches/Erina_Cache/" + file).delete()
            for file in files_in_dir(erina_dir + "/ErinaCaches/IQDB_Cache"):
                if extension_from_base(file) == ".erina":
                    TextFile(erina_dir + "/ErinaCaches/IQDB_Cache/" + file).delete()
            for file in files_in_dir(erina_dir + "/ErinaCaches/SauceNAO_Cache"):
                if extension_from_base(file) == ".erina":
                    TextFile(erina_dir + "/ErinaCaches/SauceNAO_Cache/" + file).delete()
            for file in files_in_dir(erina_dir + "/ErinaCaches/TraceMoe_Cache"):
                if extension_from_base(file) == ".erina":
                    TextFile(erina_dir + "/ErinaCaches/TraceMoe_Cache/" + file).delete()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/database/clean", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_cleanDatabase():
    """
    Cleans the database
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            for file in files_in_dir(erina_dir + "/ErinaDB/ErinaDatabase"):
                delete(erina_dir + "/ErinaDB/ErinaDatabase/" + file)
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/database/updateManami", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_verifyManami():
    """
    Updates ManamiDB
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            verify_manami_adb(force=True)
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"manami": str(ManamiDatabase)})
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/shutdown", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_shutdownServer():
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
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/api/admin/restart", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_restartServer():
    """
    Restarts ErinaServer
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina").write(authManagement.currentToken)
            Thread(target=_restart, daemon=True).start()
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))




######## UPDATES

update_status = "NOT_UPDATING"
update_message = "Erina is currently not updating"

def _update():
    """
    Updates Erina
    """
    global update_status
    global update_message
    try:
        update_status = "DOWNLOADING_UPDATE"
        update_message = "Update: Downloading the new update..."
        print(update_message)
        newErinaContent = BytesIO(requests.get("https://github.com/Animenosekai/Project_Erina/archive/master.zip").content)
        
        update_status = "BACKING_UP"
        update_message = "Update: Backing up Erina..."
        print(update_message)
        if isdir(erina_dir + "/Erina/update/keep"):
            if delete(erina_dir + "/Erina/update/keep") != 0:
                raise ErinaUpdateError("Unable to delete the previous keep folder")
        if make_dir(erina_dir + "/Erina/update/keep") == "Error while making the new folder":
            raise ErinaUpdateError("Unable to create the keep folder")

        mapping = JSONFile(erina_dir + "/Erina/update/keep_mapping.json").read()
        for fileID in mapping:
            file = mapping[fileID]
            if isdir(erina_dir + "/" + file):
                if make_dir(erina_dir + "/Erina/update/keep/" + fileID) == "Error while making the new folder":
                    raise ErinaUpdateError("Error while making a backup folder")
                copy_tree(erina_dir + "/" + file, erina_dir + "/Erina/update/keep/" + fileID)
            elif isfile(erina_dir + "/" + file):
                copyfile(erina_dir + "/" + file, erina_dir + "/Erina/update/keep/" + fileID)

        update_status = "EXTRACTING_UPDATE"
        update_message = "Update: Extracting the new update..."
        print(update_message)
        ZipFile(newErinaContent).extractall(erina_dir + "/Erina/update/archive_container")
        archiveName = None
        for file in files_in_dir(erina_dir + "/Erina/update/archive_container"):
            if "erina" in file.lower():
                archiveName = file
        if archiveName is None:
            raise ErinaUpdateError("Could not find downloaded ErinaUpdate")
        
        archivePath = erina_dir + "/Erina/update/archive_container/" + archiveName
        if TextFile(archivePath + "/Erina/update/integrity_verification.erina").read() != "ERINA_UPDATE_SUCCESSFULLY_DOWNLOADED":
            raise ErinaUpdateError("Erina update is corrupted")

        if delete(archivePath + "/Erina/update") != 0:
            raise ErinaUpdateError("An error occured while removing keep from update")

        update_status = "REPLACING_FILES"
        update_message = "Update: Replacing the files..."
        print(update_message)
        
        def mergeUpdate(dir):
            for file in files_in_dir(archivePath + dir):
                if isdir(archivePath + dir + file):
                    mergeUpdate(dir + file + "/")
                else:
                    if exists(erina_dir + dir + file):
                        delete(erina_dir + dir + file)
                    move(archivePath + dir + file, erina_dir + dir + file)

        mergeUpdate("/")

        update_status = "RESTORING_FILES"
        update_message = "Update: Restoring the files..."
        print(update_message)
        newMapping = json.loads(requests.get("https://raw.githubusercontent.com/Animenosekai/Project_Erina/master/Erina/update/keep_mapping.json").text)

        for fileID in newMapping:
            if exists(erina_dir + "/update/keep/" + fileID):
                move(erina_dir + "/update/keep/" + fileID, erina_dir + "/" + newMapping[fileID])

        
        update_status = "CLEANING"
        update_message = "Update: Cleaning the update..."
        print(update_message)
        delete(erina_dir + "/Erina/update/keep")
        delete(erina_dir + "/Erina/update/archive_container")
        

        update_status = "RESTARTING"
        update_message = "Update: Erina is restarting to finish the update..."
        print(update_message)
        TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina").write(authManagement.currentToken)
        Thread(target=_restart, daemon=True).start()
    except:
        traceback.print_exc()
        update_status = "LAST_UPDATE_FAILED"
        update_message = f"Update: The update failed ({str(exc_info()[0])})"
        print("ERINA UPDATE ERROR")
        print(update_message)

@ErinaServer.route("/erina/api/admin/update", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_updateServer():
    """
    Updates and restarts the server
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            newEnv = requests.get("https://raw.githubusercontent.com/Animenosekai/Project_Erina/master/Erina/env_information.py").text.split("\n")
            newVersion = None
            for line in newEnv:
                if line.startswith("erina_version"):
                    newVersion = line.replace(" ", "").split("=")[1].replace('"', '')
                    break
            if newVersion == erina_version.replace(" ", ""):
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "NO_UPDATE", "message": "Erina is already up to date!", "newVersion": newVersion, "currentVersion": erina_version})
            else:
                if update_status not in ["NOT_UPDATING", "LAST_UPDATE_FAILED"]:
                    return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "ALREADY_UPDATING", "message": "Erina is already updating"})    
                if import_status not in ["NOT_IMPORTING", "LAST_IMPORT_FAILED"]:
                    return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_IMPORTING", "message": "Erina is currently importing a backup"}, error="CURRENTLY_IMPORTING", code=400)
                if backup_status not in ["NOT_BACKING_UP", "LAST_BACKUP_FAILED"]:
                    return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_BACKING_UP", "message": "Erina is currently backing up"}, error="CURRENTLY_BACKING_UP", code=400)
                Thread(target=_update, daemon=True).start()
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "UPDATE_STARTED", "message": "Updating Erina..."})
                    
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/update/status")
def ErinaServer_Endpoint_Admin_Config_updateStatus():
    """
    Returns the status of the update
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": update_status, "message": update_message})
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))






######## BACKUPS
backup_status = "NOT_BACKING_UP"
backup_message = "There is currently no backup planned"

def _createBackup():
    global backup_status
    global backup_message

    try:
        backup_status = "BACKING_UP"
        backup_message = "Backup: Erina is currently preparing a backup"
        print(backup_message)
        if isdir(erina_dir + "/Erina/update/keep"):
            if delete(erina_dir + "/Erina/update/keep") != 0:
                raise ErinaUpdateError("Unable to delete the previous keep folder")
        if make_dir(erina_dir + "/Erina/update/keep") == "Error while making the new folder":
            raise ErinaUpdateError("Unable to create the keep folder")

        mapping = JSONFile(erina_dir + "/Erina/update/keep_mapping.json").read()
        for fileID in mapping:
            file = mapping[fileID]
            if isdir(erina_dir + "/" + file):
                if make_dir(erina_dir + "/Erina/update/keep/" + fileID) == "Error while making the new folder":
                    raise ErinaUpdateError("Error while making a backup folder")
                copy_tree(erina_dir + "/" + file, erina_dir + "/Erina/update/keep/" + fileID)
            elif isfile(erina_dir + "/" + file):
                copyfile(erina_dir + "/" + file, erina_dir + "/Erina/update/keep/" + fileID)

        backup_status = "ZIPPING"
        backup_message = "Backup: Erina is currently zipping the backup"
        print(backup_message)

        make_archive(erina_dir + "/ErinaServer/Erina/admin/backups/ErinaBackup", "zip", erina_dir + "/Erina/update/keep")

        backup_status = "CLEANING"
        backup_message = "Backup: Erina is currently cleaning the backup"
        print(backup_message)
        if isdir(erina_dir + "/Erina/update/keep"):
            delete(erina_dir + "/Erina/update/keep")

        backup_status = "READY_FOR_DOWNLOAD"
        backup_message = "Backup: Erina is ready to send the archive"
        print(backup_message)

    except:
        traceback.print_exc()
        backup_status = "LAST_BACKUP_FAILED"
        backup_message = f"Backup: The backup failed ({str(exc_info()[0])})"
        print("ERINA BACKUP ERROR")
        print(backup_message)

import_status = "NOT_IMPORTING"
import_message = "Erina is currently not importing any backup data"

def _importBackup(backupfile):
    global import_status
    global import_message

    try:
        if backupfile is None:
            import_status = "LAST_IMPORT_FAILED"
            import_message = "Import: The import failed (BackupFileNotFound)"
            print("ERINA IMPORT ERROR")
            print(import_message)

        update_status = "EXTRACTING_UPDATE"
        update_message = "Update: Extracting the new update..."
        print(update_message)
        ZipFile(BytesIO(b64decode(str(backupfile).replace("data:application/zip;base64,", "", 1)))).extractall(erina_dir + "/Erina/update/keep")

        import_status = "RESTORING_FILES"
        import_message = "Import: Restoring the files..."
        print(import_message)
        newMapping = JSONFile(erina_dir + "/Erina/update/keep_mapping.json").read()

        for fileID in newMapping:
            if exists(erina_dir + "/update/keep/" + fileID):
                move(erina_dir + "/update/keep/" + fileID, erina_dir + "/" + newMapping[fileID])

        
        import_status = "CLEANING"
        import_message = "Import: Cleaning the update..."
        print(import_message)
        delete(erina_dir + "/Erina/update/keep")
        delete(erina_dir + "/Erina/update/archive_container")
        

        import_status = "RESTARTING"
        import_message = "Import: Erina is restarting to finish the import..."
        print(import_message)
        TextFile(erina_dir + "/ErinaServer/Erina/auth/lastToken.erina").write(authManagement.currentToken)
        Thread(target=_restart, daemon=True).start()

    except:
        traceback.print_exc()
        import_status = "LAST_IMPORT_FAILED"
        import_message = f"Import: The import failed ({str(exc_info()[0])})"
        print("ERINA IMPORT ERROR")
        print(import_message)

#
@ErinaServer.route("/erina/api/admin/backup/import", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_backupImport():
    """
    Imports a backup archive
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if import_status not in ["NOT_IMPORTING", "LAST_IMPORT_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "ALREADY_REQUESTED", "message": "Erina is currently preparing your backup"}, error="CURRENTLY_BACKING_UP", code=400)
            if update_status not in ["NOT_UPDATING", "LAST_UPDATE_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_UPDATING", "message": "Erina is currently updating"}, error="CURRENTLY_UPDATING", code=400)
            if backup_status not in ["NOT_BACKING_UP", "LAST_BACKUP_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_BACKING_UP", "message": "Erina is currently backing up"}, error="CURRENTLY_BACKING_UP", code=400)
            if "backupBase64Data" in request.values:
                Thread(target=_importBackup, daemon=True, args=[request.values.get("backupBase64Data", None)]).start()
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "IMPORT_STARTED", "message": "Importing your backup..."})
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "ARCHIVE_NOT_RECEIVED", "message": "No ErinaBackup archive got received"}, code=400, error="ARCHIVE_NOT_RECEIVED")
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/backup/request", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_backupRequest():
    """
    Sends a backup archive
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if backup_status not in ["NOT_BACKING_UP", "LAST_BACKUP_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "ALREADY_REQUESTED", "message": "Erina is currently preparing your backup"}, error="CURRENTLY_BACKING_UP", code=400)
            if import_status not in ["NOT_IMPORTING", "LAST_IMPORT_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_IMPORTING", "message": "Erina is currently importing a backup"}, error="CURRENTLY_IMPORTING", code=400)
            if update_status not in ["NOT_UPDATING", "LAST_UPDATE_FAILED"]:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "CURRENTLY_UPDATING", "message": "Erina is currently updating"}, error="CURRENTLY_UPDATING", code=400)
            Thread(target=_createBackup, daemon=True).start()
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": "BACKUP_STARTED", "message": "Preparing your backup..."})
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/backup/status")
def ErinaServer_Endpoint_Admin_Config_backupStatus():
    """
    Returns the status of the backup
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": backup_status, "message": backup_message})
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/backup/download")
def ErinaServer_Endpoint_Admin_Config_backupDownload():
    """
    Returns the content of the backup
    """
    global backup_status
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if backup_status == "READY_FOR_DOWNLOAD":
                backup_status = "NOT_BACKING_UP"
                return send_from_directory(erina_dir + "/ErinaServer/Erina/admin/backups/", "ErinaBackup.zip")
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": backup_status, "message": backup_message}, error="NOT_READY_YET", code=204)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/import/status")
def ErinaServer_Endpoint_Admin_Config_importStatus():
    """
    Returns the status of the import
    """
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"status": import_status, "message": import_message})
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))


@ErinaServer.route("/erina/alive")
@ErinaRateLimit(0.1)
def ErinaServer_Endpoint_Admin_Config_alive():
    """
    Returns an answer if ErinaServer is alive
    """
    return json.dumps({"message": "Yes, I'm alive!", "success": True}, ensure_ascii=False), 200


@ErinaServer.route("/erina/api/admin/information")
def ErinaServer_Endpoint_Admin_Config_information():
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            platformInfo = platform.uname()
            results = {
                "version": "ErinaServer " + str(erina_version),
                "installed_directory": str(erina_dir),
                "python_version": "Python " + str(python_version_info.major) + "." + str(python_version_info.minor) + "." + str(python_version_info.micro),
                "pid": str(pid),
                "system": str(platformInfo.system) + " (" + platformInfo.release + ")"
            }
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=results)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/state")
def ErinaServer_Endpoint_Admin_Config_state():
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            memUsage = psutil.virtual_memory()
            diskUsage = psutil.disk_usage('/')
            results = {}
            try:
                results["cpu_count"] = str(cpu_count)
            except:
                results["cpu_count"] = "N/A"
            try:
                results["cpu_frequency"] = str(psutil.cpu_freq().current) + "Mhz"
            except:
                results["cpu_frequency"] = "N/A"
            try:
                results["cpu_usage"] = str(psutil.cpu_percent()) + "%"
            except:
                results["cpu_usage"] = "N/A"
            try:
                results["ram_usage_used"] = str(get_scaled_size(memUsage.used))
            except:
                results["ram_usage_used"] = "N/A"
            try:
                results["ram_usage_total"] = str(get_scaled_size(memUsage.total))
            except:
                results["ram_usage_total"] = "N/A"
            try:
                results["ram_usage_percentage"] = str(memUsage.percent) + "%"
            except:
                results["ram_usage_percentage"] = "N/A"
            try:
                results["disk_usage_used"] = str(get_scaled_size(diskUsage.used))
            except:
                results["disk_usage_used"] = "N/A"
            try:
                results["disk_usage_total"] = str(get_scaled_size(diskUsage.total))
            except:
                results["disk_usage_total"] = "N/A"
            try:
                results["disk_usage_percentage"] = str(diskUsage.percent) + "%"
            except:
                results["disk_usage_percentage"] = "N/A"
            try:
                results["disk_total_read"] = str(get_scaled_size(psutil.disk_io_counters().read_bytes))
            except:
                results["disk_total_read"] = "N/A"
            try:
                results["disk_total_write"] = str(get_scaled_size(psutil.disk_io_counters().write_bytes))
            except:
                results["disk_total_write"] = "N/A"
            try:
                results["net_total_sent"] = str(get_scaled_size(psutil.net_io_counters().bytes_sent))
            except:
                results["net_total_sent"] = "N/A"
            try:
                results["net_total_received"] = str(get_scaled_size(psutil.net_io_counters().bytes_recv))
            except:
                results["net_total_received"] = "N/A"
            try:
                results["threads"] = current_threads()
            except:
                results["threads"] = "N/A"
            return makeResponse(token_verification=tokenVerification, request_args=request.values, data=results)
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

@ErinaServer.route("/erina/api/admin/twitter/checkTweet", methods=["POST"])
def ErinaServer_Endpoint_Admin_Config_checkTweet():
    tokenVerification = authManagement.verifyToken(request.values)
    try:
        if tokenVerification.success:
            if "tweet" in request.values:
                tweetID = urlparse(request.values.get("tweet")).path.split("/")[-1]
                tweet = ErinaTwitter.api.get_status(tweetID)
                ErinaStreamListener.on_status(tweet, force=True)
                return makeResponse(token_verification=tokenVerification, request_args=request.values, data={"message": "Successfully sent the tweet to ErinaTwitter"})
            else:
                return makeResponse(token_verification=tokenVerification, request_args=request.values, error="MISSING_ARGS", data={"authorizedArgs": ["tweet", "minify"], "optionalArgs": ["minify"]}, code=400, error_message="No Tweet URL were sent")
        else:
            return makeResponse(token_verification=tokenVerification, request_args=request.values)
    except:
        traceback.print_exc()
        return makeResponse(token_verification=tokenVerification, request_args=request.values, code=500, error=str(exc_info()[0]))

