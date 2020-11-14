import json
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

config = None


def makeResponse(success, loggedIn, message, data):
    return json.dumps({"success": success, "loggedIn": loggedIn, "message": message, "data": data, "server": "ErinaSauce", "category": "ErinaAdmin"})

@app.route("/erina/api/admin", methods=["GET"])
def admin_data():
    if "Erina-Account-Password" in request.headers:
        if request.headers.get("Erina-Account-Password") == config.admin_password:
            return makeResponse(True, True, "Success", {"html": None})
        else:
            return makeResponse(False, False, "You are not logged in", None)
    else:
        return makeResponse(False, False, "The Erina-Account-Password header is missing", None)

@app.route("/erina/login", methods=["GET"])
def login():
    return render_template("/static/login/login.html")

@app.route("/erina/assets/login.css", methods=["GET"])
def login():
    return render_template("/static/login/login.css")

@app.route("/erina/admin", methods=["GET"])
def admin():
    return render_template("/static/admin/admin.html")

@app.route("/erina/assets/admin.css", methods=["GET"])
def admin():
    return render_template("/static/admin/admin.css")