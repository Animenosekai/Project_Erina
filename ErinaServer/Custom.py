from ErinaServer.Server import ErinaServer, ErinaRateLimit, ErinaStats
from ErinaServer.WebSockets import ErinaSockets

@ErinaServer.route("/keepalive", methods=["GET"])
@ErinaRateLimit()
@ErinaStats("Keep Alive")
def noSleep():
    return '{"message": "success"}', 200

