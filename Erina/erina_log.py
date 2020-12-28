"""
Logging utility for Erina

Erina Project
© Anime no Sekai - 2020
"""

from sys import platform
from os import system
from time import time, sleep

from safeIO import TextFile

from Erina import config
from Erina.env_information import erina_dir
from ErinaServer.WebSockets import ErinaSockets
from ErinaServer.Erina.auth import authManagement
import json

logFile = TextFile(erina_dir + "/Erina/logs/logs.erinalog", blocking=False)
errorsFile = TextFile(erina_dir + "/Erina/logs/errors.erinalog", blocking=False)

def log(api, message, error=False):
    """
    Logs something
    """
    message = str(message)
    if config.Erina.console_log:
        if not error:
            print(f"[{api}] {message}")
        else:
            print("[Error] [" + api + "] " + message)
    timestamp = int(time())
    if config.Erina.file_log:
        if not error:
            logFile.append(f"{str(timestamp)}    [{api}] {str(message)}".replace("\n", "") + "\n")
        else:
            logFile.append(f"{str(timestamp)}    [Error]    [{api}] {str(message)}".replace("\n", "") + "\n")
    try:
        if platform == "darwin" and error:
            system("osascript -e 'display notification \"{}\" with title \"{}\"'".format(f"[{api}] {message}", "ErinaServer Error"))
    except:
        pass
    sendLogToConnections(api=api, message=message, timestamp=timestamp, error=error)

def _checkForLogsTimeout(logsContent):
    removingLineIndex = 0
    timeout = config.Erina.logs_timeout
    for line in logsContent:
        if time() - float(line.split("    ")[0]) >= timeout:
            removingLineIndex += 1
        else:
            break
    logFile.blocking = True
    logFile.writelines(logFile.readlines()[removingLineIndex:])
    logFile.blocking = False

def checkForLogsTimeout():
    logFile.readlines(callback=_checkForLogsTimeout)



currentConnections = []

@ErinaSockets.route("/erina/websockets/Logs")
def ErinaServer_Endpoint_Erina_Logs_WebSocketLogs(ws):
    message = ws.receive()
    try:
        data = json.loads(message) # retrieve a message from the client
        if "token" in data:
            tokenVerification = authManagement.verifyToken(data)
            if tokenVerification.success:
                currentConnections.append(ws)
                ws.send(json.dumps({"api": "ErinaAdmin", "message": "Successfully connected to ErinaLogs", "error": False, "timestamp": int(time())}))
            else:
                ws.send(json.dumps({"api": "ErinaAdmin", "message": f"ErinaLogs: Authentification Error: {str(tokenVerification)}", "error": True, "timestamp": int(time())}))
        else:
            ws.send(json.dumps({"api": "ErinaAdmin", "message": "ErinaLogs: Your connection could not be authentificated", "error": True, "timestamp": int(time())}))
    except:
        try:
            ws.send(json.dumps({"api": "ErinaAdmin", "message": "ErinaLogs: Your connection could not be authentificated", "error": True, "timestamp": int(time())}))
        except:
            log("ErinaAdmin", "ErinaConsole >>> Failed to send a message")

    try:
        while not ws.closed:
            try:
                ws.receive()
            except:
                currentConnections.remove(ws)
    except:
        currentConnections.remove(ws)    
    
    if ws in currentConnections:
        currentConnections.remove(ws)

def sendLogToConnections(api, message, timestamp, error=False):
    for connection in currentConnections:
        connection.send(json.dumps({"api": api, "message": message, "error": error, "timestamp": timestamp}))