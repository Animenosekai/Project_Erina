"""
Logging utility for Erina

Erina Project
© Anime no Sekai - 2020
"""

from time import time, sleep
from threading import Thread

from safeIO import TextFile

from Erina import config
from Erina.env_information import erina_dir

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
    if config.Erina.file_log:
        if not error:
            logFile.append(f"{str(int(time()))}    [{api}] {str(message)}".replace("\n", "") + "\n")
        else:
            logFile.append(f"{str(int(time()))}    [Error]    [{api}] {str(message)}".replace("\n", "") + "\n")

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