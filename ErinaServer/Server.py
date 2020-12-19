from flask import Flask
from Erina.config import Server

if Server.disable_console_messages:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

ErinaServer = Flask(__name__)
