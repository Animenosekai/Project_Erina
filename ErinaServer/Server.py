from flask import Flask
from Erina.config import Server

ErinaServer = Flask(__name__)


if Server.disable_console_messages:
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)