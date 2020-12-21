"""
Erina Clients Wrapper for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""
if __name__ == '__main__':

    #### INITIALIZING ERINASERVER --> Manages the whole server
    from threading import Thread
    from Erina.erina_log import log, logFile

    log("Erina", "Initializing Erina configuration...")
    from Erina.config import Server as ServerConfig
    log("Erina", "Initializing ErinaServer")
    from ErinaServer.Server import ErinaServer
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler


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
    log("Erina", "---> Initializing the WebSocket Endpoints")
    from ErinaServer.Erina.admin.console import console

    def runServer():
        ## RUNNING ErinaServer
        log("Erina", "Running ErinaServer...")
        ErinaWSGIServer = pywsgi.WSGIServer((ServerConfig.host, ServerConfig.port), ErinaServer, handler_class=WebSocketHandler)
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

    Thread(target=runClients, daemon=True).start()

    try:
        runServer()
    except KeyboardInterrupt:
        logFile.blocking = True
        log("Erina", "Goodbye!")        
