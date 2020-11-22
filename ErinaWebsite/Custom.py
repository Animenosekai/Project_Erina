from ErinaWebsite.Server import ErinaServer

@ErinaServer.route("/hey", methods=["GET"])
def Hey():
    return "Hey"