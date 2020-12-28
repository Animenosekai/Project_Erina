
from flask import send_from_directory, redirect, request
from Erina.env_information import erina_dir
from ErinaServer.Server import ErinaServer
from ErinaServer.Erina.auth import authManagement

staticLocation = erina_dir + "/ErinaServer/Erina/static"
htmlLocation = staticLocation + "/html"
stylesLocation = staticLocation + "/styles"
scriptsLocation = staticLocation + "/scripts"
imagesLocation = staticLocation + "/images"
faviconsLocation = staticLocation + "/images/favicons"

scriptsPath = "/erina/admin/static/scripts/"
stylesPath = "/erina/admin/static/styles/"

#######################
#         HTML        #
#######################

@ErinaServer.route("/erina/admin/<page>")
def ErinaServer_Endpoint_Static_mainEndpoint(page):
    try:
        if str(page) == "login":
            return send_from_directory(htmlLocation, "login.html")
        elif str(page) in ["", "overview", "api", "stats", "config"]:
            return send_from_directory(htmlLocation, "main.html")
        else:
            return send_from_directory(htmlLocation, "404.html"), 404
    except:
        return send_from_directory(htmlLocation, "500.html"), 500

@ErinaServer.route("/erina/admin/")
def ErinaServer_Endpoint_Static_redirectToMainEndpoint():
    try:
        return send_from_directory(htmlLocation, "main.html")
    except:
        return send_from_directory(htmlLocation, "500.html"), 500
        
@ErinaServer.route("/erina/admin/static/styles/<page>.css")
def ErinaServer_Endpoint_Static_stylesEndpoint(page):
    try:
        if page in ["main", "console", "loading", "overview", "stats", "config", "api", "infoBox"]:
            return send_from_directory(stylesLocation, page + ".css")
        elif page == "login":
            return send_from_directory(stylesLocation, "login.css")
        return send_from_directory(htmlLocation, "404.html"), 404
    except:
        return send_from_directory(htmlLocation, "500.html"), 500
        
@ErinaServer.route("/erina/admin/static/scripts/<page>.js")
def ErinaServer_Endpoint_Static_scriptsEndpoint(page):
    try:
        if page in ["main", "console", "loading", "chart", "overview", "stats", "config", "api"]:
            return send_from_directory(scriptsLocation, page + ".js")
        elif page == "login":
            return send_from_directory(scriptsLocation, "login.js")
        return send_from_directory(htmlLocation, "404.html"), 404
    except:
        return send_from_directory(htmlLocation, "500.html"), 500


@ErinaServer.route("/erina/admin/static/images/404-Chan")
def ErinaServer_Endpoint_Static_NotFound():
    return send_from_directory(imagesLocation, "404-Chan.png")

@ErinaServer.route("/erina/admin/static/images/500-Chan")
def ErinaServer_Endpoint_Static_ServerError():
    return send_from_directory(imagesLocation, "500-Chan.png")

@ErinaServer.route("/erina/admin/static/images/Tenshi")
def ErinaServer_Endpoint_Static_Tenshi():
    return send_from_directory(imagesLocation, "Tenshi.png")



##### FAVICONS
@ErinaServer.route("/favicon.ico")
def ErinaServer_Endpoint_Static_favicon():
    return send_from_directory(faviconsLocation, "favicon.ico")

@ErinaServer.route("/apple-touch-icon.png")
def ErinaServer_Endpoint_Static_favicon_appleTouchIcon():
    return send_from_directory(faviconsLocation, "apple-touch-icon.png")

@ErinaServer.route("/favicon-32x32.png")
def ErinaServer_Endpoint_Static_favicon_favicon32by32():
    return send_from_directory(faviconsLocation, "favicon-32x32.png")

@ErinaServer.route("/favicon-16x16.png")
def ErinaServer_Endpoint_Static_favicon_favicon16by16():
    return send_from_directory(faviconsLocation, "favicon-16x16.png")

@ErinaServer.route("/site.webmanifest")
def ErinaServer_Endpoint_Static_favicon_siteWebmanifest():
    return send_from_directory(faviconsLocation, "site.webmanifest")

@ErinaServer.route("/safari-pinned-tab.svg")
def ErinaServer_Endpoint_Static_favicon_safariPinnedTab():
    return send_from_directory(faviconsLocation, "safari-pinned-tab.svg")

@ErinaServer.route("/android-chrome-192x192.png")
def ErinaServer_Endpoint_Static_favicon_androidChrome192by192():
    return send_from_directory(faviconsLocation, "android-chrome-192x192.png")

@ErinaServer.route("/android-chrome-512x512.png")
def ErinaServer_Endpoint_Static_favicon_androidChrome512by512():
    return send_from_directory(faviconsLocation, "android-chrome-512x512.png")