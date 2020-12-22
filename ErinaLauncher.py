"""
Erina Clients Wrapper for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

import sys

def shutdownErinaServer(num, info):
    ErinaWSGIServer.stop()
    ErinaWSGIServer.close()
    logFile.blocking = True
    log("Erina", "Goodbye!")
    sys.exit(0)
    

if __name__ == '__main__':

    #### INITIALIZING ERINASERVER --> Manages the whole server
    print("[Erina]", "Initializing ErinaServer")
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
            from ErinaDiscord.erina_discordbot import client as discordClient
            asyncio.get_event_loop().create_task(discordClient.start(config.Discord.keys.token))
            asyncio.get_event_loop().run_forever()

    from threading import Thread
    Thread(target=runClients, daemon=True).start()

    import signal
    from sys import exc_info
    signal.signal(signal.SIGINT, shutdownErinaServer)
    signal.signal(signal.SIGTERM, shutdownErinaServer)

    try:
        runServer()
    except:
        logFile.blocking = True
        log("Erina", f"An error occured while running ErinaServer ({exc_info()[0]})", True)