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

def verifyToken(args):
    if "token" in args:
        return authManagement.verifyToken(args.get("token"))
    else:
        return None


@ErinaServer.route("/erina/admin/resource/<page>/")
def resourceEndpoint(page):
    if page in ["overview", "api", "stats", "config"]:
        tokenVerification = verifyToken(request.values)
        if tokenVerification is not None:
            if tokenVerification.success:
                return send_from_directory(htmlLocation, page + ".html")
            else:
                return "ErinaAdminLoginRedirect"
        else:
            return "ErinaAdminLoginRedirect"
    else:
        return "404, Not Found"