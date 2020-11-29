from flask import request
from flask import redirect
from flask import send_from_directory
from ErinaWebsite.Server import ErinaServer
from ErinaWebsite.Erina.auth import authManagement
from env_information import erina_dir

resourcePath = "/erina/admin/resource/"
frontEndPath = "/erina/admin/"

staticLocation = erina_dir + "/ErinaWebsite/Erina/static"
htmlLocation = staticLocation + "/html"

def verifyToken(args):
    if "token" in args:
        return authManagement.verifyToken(args.get("token"))
    else:
        return None

@ErinaServer.route(resourcePath + "overview")
def resourceOverview():
    tokenVerification = verifyToken(request.values)
    if tokenVerification is not None:
        if tokenVerification.success:
            return send_from_directory(htmlLocation, "overview.html")
        else:
            return "ErinaAdminLoginRedirect"

@ErinaServer.route(resourcePath + "stats")
def resourceStats():
    tokenVerification = verifyToken(request.values)
    if tokenVerification is not None:
        if tokenVerification.success:
            return "Stats Page"
        else:
            return "ErinaAdminLoginRedirect"

@ErinaServer.route(resourcePath + "api")
def resourceApi():
    tokenVerification = verifyToken(request.values)
    if tokenVerification is not None:
        if tokenVerification.success:
            return "API Page"
        else:
            return "ErinaAdminLoginRedirect"

@ErinaServer.route(resourcePath + "config")
def resourceConfig():
    tokenVerification = verifyToken(request.values)
    if tokenVerification is not None:
        if tokenVerification.success:
            return "Config Page"
        else:
            return "ErinaAdminLoginRedirect"