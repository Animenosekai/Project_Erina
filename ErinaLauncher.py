"""
Erina Clients Wrapper for the Erina Project

@author: Anime no Sekai
Erina Project - 2020
"""

from time import sleep


if __name__ == '__main__':

    #### INITIALIZING ERINASERVER --> Manages the whole server

    from threading import Thread
    from Erina.erina_log import log, logFile

    log("Erina", "Initializing Erina configuration...")
    from Erina.config import Server as ServerConfig
    from Erina.env_information import cpu_count
    log("Erina", "Initializing ErinaServer")
    from ErinaServer.Server import ErinaServer
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    import gunicorn.app.base

    class ErinaServerGunicorn(gunicorn.app.base.BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                    if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

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
        ## RUNNING ErinaServer (HTTP)
        log("Erina", "Running ErinaServer...")
        
        options = {
            'bind': f"{str(ServerConfig.host)}:{str(ServerConfig.port)}",
            'workers': (cpu_count * 2) + 1,
            'worker-class': "flask_sockets.worker",
            "reload": False,
            "proc_name": "ErinaServer",
            "preload_app": True,

        }
        ErinaServerGunicorn(ErinaServer, options).run()
        
        """
        ErinaWSGIServer = pywsgi.WSGIServer((ServerConfig.host, ServerConfig.port), ErinaServer, handler_class=WebSocketHandler)
        ErinaWSGIServer.serve_forever()
        """


    #### RUNNING THE CLIENTS
    

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

    """
    try:
        while True: # Block
            sleep(3600)
    except KeyboardInterrupt:
        logFile.blocking = True
        log("Erina", "Goodbye!")
    """