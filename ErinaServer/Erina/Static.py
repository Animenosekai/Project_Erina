
from flask import send_from_directory
from Erina.env_information import erina_dir
from ErinaServer.Server import ErinaServer

staticLocation = erina_dir + "/ErinaServer/Erina/static"
htmlLocation = staticLocation + "/html"
stylesLocation = staticLocation + "/styles"
scriptsLocation = staticLocation + "/scripts"

scriptsPath = "/erina/admin/static/scripts/"
stylesPath = "/erina/admin/static/styles/"


#######################
#         HTML        #
#######################

@ErinaServer.route("/erina/admin/<page>")
def mainEndpoint(page):
    print(page)
    if str(page) == "login":
        return "Login Page"
    elif str(page) in ["", "overview", "api", "stats", "config"]:
        return send_from_directory(htmlLocation, "main.html")
    else:
        return "404, Not Found"


@ErinaServer.route("/erina/admin/static/styles/<page>.css")
def stylesEndpoint(page):
    if page in ["main", "console", "loading", "overview", "stats", "config", "api", "infoBox"]:
        return send_from_directory(stylesLocation, page + ".css")
    return "404, Not Found"

@ErinaServer.route("/erina/admin/static/scripts/<page>.js")
def scriptsEndpoint(page):
    if page in ["main", "console", "loading", "chart", "overview", "stats", "config", "api"]:
        return send_from_directory(scriptsLocation, page + ".js")
    return "404, Not Found"