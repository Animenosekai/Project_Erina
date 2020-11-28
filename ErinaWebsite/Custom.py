from ErinaWebsite.Server import ErinaServer

@ErinaServer.route("/keepalive", methods=["GET"])
def noSleep():
    return '{"message": "success"}', 200

