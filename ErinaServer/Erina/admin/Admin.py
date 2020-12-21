from flask import request
from flask import redirect
from flask import send_from_directory
from ErinaServer.Server import ErinaServer
from ErinaServer.Erina.auth import authManagement
from Erina.env_information import erina_dir

resourcePath = ""
frontEndPath = "/erina/admin/"

staticLocation = erina_dir + "/ErinaServer/Erina/static"
htmlLocation = staticLocation + "/html"

@ErinaServer.route("/erina/admin/resource/<page>/")
def resourceEndpoint(page):
    if page in ["overview", "api", "stats", "config"]:
        tokenVerification = authManagement.verifyToken(request.values)
        if tokenVerification.success:
            return send_from_directory(htmlLocation, page + ".html")
        else:
            print(str(tokenVerification))
            return "ErinaAdminLoginRedirect"
    else:
        return send_from_directory(htmlLocation, "404-Chan.html")