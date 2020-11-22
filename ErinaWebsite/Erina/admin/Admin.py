from flask import request
from flask import redirect
from ErinaWebsite.Server import ErinaServer
from ErinaWebsite.Erina.auth import authManagement

resourcePath = "/erina/admin/resource/"
frontEndPath = "/erina/admin/"

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
            return "Overview Page"
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