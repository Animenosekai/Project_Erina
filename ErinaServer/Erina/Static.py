
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


#######################
#        Styles       #
#######################

@ErinaServer.route(stylesPath + "main.css")
def mainCss():
    return send_from_directory(stylesLocation, "main.css")

@ErinaServer.route(stylesPath + "console.css")
def consoleCss():
    return send_from_directory(stylesLocation, "console.css")

@ErinaServer.route(stylesPath + "loading.css")
def loadingCss():
    return send_from_directory(stylesLocation, "loading.css")

@ErinaServer.route(stylesPath + "overview.css")
def overviewCss():
    return send_from_directory(stylesLocation, "overview.css")

@ErinaServer.route(stylesPath + "stats.css")
def statsCss():
    return send_from_directory(stylesLocation, "stats.css")

@ErinaServer.route(stylesPath + "config.css")
def configCss():
    return send_from_directory(stylesLocation, "config.css")

#######################
#      JavaScript     #
#######################
@ErinaServer.route(scriptsPath + "main.js")
def mainJs():
    return send_from_directory(scriptsLocation, "main.js")

@ErinaServer.route(scriptsPath + "console.js")
def consoleJs():
    return send_from_directory(scriptsLocation, "console.js")

@ErinaServer.route(scriptsPath + "loading.js")
def loadingJs():
    return send_from_directory(scriptsLocation, "loading.js")

@ErinaServer.route(scriptsPath + "chart.js")
def chartJs():
    return send_from_directory(scriptsLocation, "chart.js")

@ErinaServer.route(scriptsPath + "overview.js")
def overviewJs():
    return send_from_directory(scriptsLocation, "overview.js")

@ErinaServer.route(scriptsPath + "stats.js")
def statsJs():
    return send_from_directory(scriptsLocation, "stats.js")

@ErinaServer.route(scriptsPath + "config.js")
def configJs():
    return send_from_directory(scriptsLocation, "config.js")