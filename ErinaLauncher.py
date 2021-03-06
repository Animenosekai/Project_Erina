"""
Erina Clients Wrapper for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

from safeIO import TextFile
from ErinaLine.erina_linebot import initHandler
import os
import sys
import psutil
import traceback
from Erina.env_information import erina_dir

"""
import logging
logging.basicConfig(level=logging.DEBUG)
"""

def shutdownErinaServer(num, info):
    """
    SIGTERM, SIGQUIT, SIGINT signals handler --> Shutdowns Erina
    """
    try:
        for handler in psutil.Process(os.getpid()).open_files():
            os.close(handler.fd)
    except:
        pass
    TextFile(erina_dir + "/launch.erina").write("0")

    ErinaWSGIServer.stop()
    ErinaWSGIServer.close()
    logFile.blocking = True
    log("Erina", "Goodbye!")

def restartErinaServer(num, info):
    """
    SIGUSR1 signal handler --> Restarts Erina
    """
    try:
        for handler in psutil.Process(os.getpid()).open_files():
            os.close(handler.fd)
    except:
        pass

    from ErinaTwitter.utils.Stream import lastDM
    from ErinaTwitter.utils.Stream import sinceID
    TextFile(erina_dir + "/ErinaTwitter/lastDM.erina").write(str(lastDM))
    TextFile(erina_dir + "/ErinaTwitter/lastStatusID.erina").write(str(sinceID))
    TextFile(erina_dir + "/launch.erina").write("0")

    ErinaWSGIServer.stop()
    ErinaWSGIServer.close()
    logFile.blocking = True
    log("Erina", "Restarting...")
    os.execl(sys.executable, sys.executable, __file__, *sys.argv[1:])
    

if __name__ == '__main__' or TextFile(erina_dir + "/launch.erina").read().replace(" ", "") in ["", "0"]:
    TextFile(erina_dir + "/launch.erina").read() == "1"

    #### INITIALIZING ERINASERVER --> Manages the whole server
    print("[Erina]", "Initializing ErinaServer")
    import requests
    import requests.packages.urllib3.contrib.pyopenssl as requestsPyOpenSSL
    requestsPyOpenSSL.extract_from_urllib3()
    from ErinaServer.Server import ErinaServer
    from ErinaServer import WebSockets
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    

    from Erina.erina_log import log, logFile
    log("Erina", "Initializing Erina configuration...")
    from Erina.config import Server as ServerConfig
    from Erina.env_information import erina_version

    ## RECORDING Endpoints
    log("Erina", "---> Initializing Static File Endpoints")
    from ErinaServer.Erina import Static
    log("Erina", "---> Initializing API")
    from ErinaServer.Erina.api import API
    log("Erina", "---> Initializing ErinaAdmin")
    from ErinaServer.Erina.admin import Admin
    from ErinaServer.Erina.auth import Auth
    from ErinaServer.Erina.admin import Config
    log("Erina", "---> Initializing Custom Endpoints")
    from ErinaServer import Custom
    log("Erina", "---> Initializing ErinaConsole")
    from ErinaServer.Erina.admin import Console

    def runServer():
        global ErinaWSGIServer
        ## RUNNING ErinaServer
        log("Erina", "Running ErinaServer...")
        wsgiEnv = {
            'SERVER_SOFTWARE': 'ErinaServer ' + erina_version,
            'wsgi.multithread': True,
            'wsgi.run_once': False
        }
        ErinaWSGIServer = pywsgi.WSGIServer((ServerConfig.host, ServerConfig.port), ErinaServer, handler_class=WebSocketHandler, environ=wsgiEnv)
        ErinaWSGIServer.serve_forever()

    def runClients():
        import asyncio
        from Erina import config
        import ErinaLine.erina_linebot # Already runs the LINE Client
        log("Erina", "Starting to check for timeouts and updates...")
        from Erina import setInterval # Already runs the checkers
        
        if config.Twitter.run:
            log("Erina", "Running the ErinaTwitter Client...")
            from ErinaTwitter.utils import Stream as twitterClient
            Thread(target=twitterClient.startStream, daemon=True).start()

        if config.Discord.run:
            log("Erina", "Running the ErinaDiscord Client...")
            from ErinaDiscord.erina_discordbot import startDiscord
            startDiscord()

        if config.Line.run:
            initHandler()

    from threading import Thread
    Thread(target=runClients, daemon=True).start()

    import signal
    from sys import exc_info
    signal.signal(signal.SIGINT, shutdownErinaServer)
    signal.signal(signal.SIGTERM, shutdownErinaServer)
    signal.signal(signal.SIGQUIT, shutdownErinaServer)
    signal.signal(signal.SIGUSR1, restartErinaServer)

    try:
        runServer()
    except:
        logFile.blocking = True
        log("Erina", f"An error occured while running ErinaServer ({exc_info()[0]})", True)
        traceback.print_exc()