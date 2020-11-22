import json
from flask import request
from flask import render_template

import env_information
from ErinaWebsite.Server import ErinaServer
from ErinaWebsite.Erina.auth import authManagement

resourcePath = "/erina/admin/resource/"
frontEndPath = "/erina/admin/"

@ErinaServer.route(resourcePath + "overview")
def resourceOverview():
    requestArgs = request.values
    if "token" in requestArgs:
        tokenVerification = authManagement.verifyToken(requestArgs.get("token"))
        if tokenVerification.success:
            return render_template(env_information.erina_dir + "/ErinaWebsites/")