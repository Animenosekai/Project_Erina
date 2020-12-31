############ DATA ############

jsonData = """{
    "Erina": {
        "flags": [
            "what is this anime", 
            "what's this anime", 
            "anime sauce", 
            "anime source", 
            "what anime this is", 
            "what anime is this", 
            "called this anime", 
            "name of this anime", 
            "what's that anime", 
            "what anime is it", 
            "name of anime", 
            "sauce to that anime"
        ], 
        "consoleLog": true, 
        "fileLog": true, 
        "stats": true,
        "logsTimeout": 604800
    }, 
    "Twitter": {
        "run": false, 
        "ignoredUsers": [], 
        "flags": [], 
        "ignoreRT": true, 
        "imagePreview": false,
        "checkMentions": false,
        "checkDM": false,
        "keys": {
            "consumerKey": null, 
            "consumerSecret": null, 
            "accessTokenKey": null, 
            "accessTokenSecret": null
        }, 
        "stream": {
            "languages": [
                "en"
            ], 
            "flags": []
        }, 
        "monitoring": {
            "accounts": [], 
            "checkReplies": false
        }
    }, 
    "Discord": {
        "run": false, 
        "flags": [], 
        "keys": {
            "token": null
        }
    }, 
    "Line": {
        "run": false, 
        "flags": [], 
        "keys": {
            "channelAccessToken": null, 
            "channelSecret": null
        }, 
        "imagesTimeout": 3600
    }, 
    "Caches": {
        "encoding": "utf-8",
        "anilistExpiration": 604800,
        "keys": {
            "tracemoe": null, 
            "saucenao": null
        }
    }, 
    "Database": {}, 
    "Hash": {
        "algorithm": "Average Hash"
    }, 
    "Parser": {}, 
    "Search": {
        "thresholds": {
            "erinaSimilarity": 100, 
            "tracemoeSimilarity": 90, 
            "saucenaoSimilarity": 90, 
            "iqdbSimilarity": 90
        }
    }, 
    "Server": {
        "host": "127.0.0.1", 
        "port": 5000, 
        "publicAPI": true
    }
}
"""


newCategory = """
<div class="expandableItem">
    <div class="expandableItem-tab">
        <input id="expandableItem-input-{expandableID}" type="checkbox" class="expandableItem-input" name="expandableItem">
        <label for="expandableItem-input-{expandableID}" class="expandableItem-label"></label>
        <div class="expandableItem-content">
            <div class="expandableItem-info">
                <span class="expandableItem-name">{categoryName}</span>
            </div>
        </div>

        <div class="expandableItem-tab-content">
            {content}
        </div>
    </div>
</div>

"""


newTagContainer = """

    <erinaconfig-list-item class="erinaConfig-ListItem">
        <erinaconfig-list-item-title>{title}</erinaconfig-list-item-title>
        <div class="tag-container" id="tagsContainer-{containerID}" config-path="{config_path}">
            <input onkeypress="return tagInputCallback(event, this)" config-path="{config_path}" placeholder="Add new..."></input>
        </div>
    </erinaconfig-list-item>

"""

newBooleanContainer = """
    <erinaconfig-list-item class="erinaConfig-ListItem">
        <erinaconfig-list-item-title>{title}</erinaconfig-list-item-title>
        <erinaconfig-list-item-value-container>
            <div class="neumorphism-toggle">
                <input type="checkbox" onclick="checkboxHandler(this);" config-path="{config_path}" id="toggle-{toggleID}">
                <label for="toggle-{toggleID}">
                    <div class="switch">
                        <div class="dot"></div>
                    </div>
                    <span id="toggleText-{toggleID}">Disabled</span>
                </label>
            </div>
        </erinaconfig-list-item-value-container>
    </erinaconfig-list-item>

"""

newTextContainer = """
    <erinaconfig-list-item class="erinaConfig-ListItem">
        <erinaconfig-list-item-title>{title}</erinaconfig-list-item-title>
        <erinaconfig-list-item-value-container>
            <input type="input" onkeypress="return textInputHandler(event, this)" class="textValueContainer textInput" placeholder="No value (click to add)" config-path="{config_path}" id='{inputID}'/>
        </erinaconfig-list-item-value-container>
    </erinaconfig-list-item>
"""

############ IMPORTS ############

import re
import json

htmlResult = """<link rel="stylesheet" href="/erina/admin/static/styles/config.css">
<import id="ErinaExternalJS-Sources" style="display: none;">
    [
        "/erina/admin/static/scripts/config.js"
    ]
</import>

<category-title>Categories</category-title>

"""

jsResult = ""

############ FUNCTIONS ############

def formatTitle(string):
    result = re.sub(r"(\w)([A-Z])", r"\1 \2", string)
    return result[0].upper() + result[1:]

def addToJS(string):
    global jsResult
    jsResult += str(string) + ";\n"

############ PARSING ############

data = json.loads(jsonData)

for category in data:
    currentConfig = data[category]
    categoryResult = ""
    for element in currentConfig:
        configPath = f"{str(category)}/{str(element)}"
        currentElement = currentConfig[element]
        
        if isinstance(currentElement, dict):
            currentResult = ""
            for child in currentElement:
                configPath = f"{str(category)}/{str(element)}/{str(child)}"
                currentChild = currentElement[child]

                if isinstance(currentChild, list):
                    currentResult += newTagContainer.format(title=formatTitle(child), config_path=configPath, containerID=configPath.replace("/", "").lower())
                    addToJS("for (element in data." + configPath.replace("/", ".") + ") { createNewTag(document.getElementById('tagsContainer-" + configPath.replace("/", "").lower() + "'), data." + configPath.replace("/", ".") + "[element]) }")
                elif isinstance(currentChild, bool):
                    currentResult += newBooleanContainer.format(title=formatTitle(child), toggleID=configPath.replace("/", "").lower(), config_path=configPath)
                    addToJS("if (data." + configPath.replace("/", ".") + " == true) { document.getElementById('toggle-" + configPath.replace("/", "").lower() + "').checked = true; document.getElementById('toggleText-" + configPath.replace("/", "").lower() + "').innerText = 'Enabled' }")
                else:
                    currentResult += newTextContainer.format(title=formatTitle(child), config_path=configPath, inputID=configPath.replace("/", "").lower())
                    addToJS("document.getElementById('" + configPath.replace("/", "").lower() + "').value = data." + configPath.replace("/", "."))
            
            categoryResult += newCategory.format(expandableID=configPath.replace("/", "").lower(), categoryName=formatTitle(element), content=currentResult)

        elif isinstance(currentElement, list):
            configPath = f"{str(category)}/{str(element)}"
            categoryResult += newTagContainer.format(title=formatTitle(element), config_path=configPath, containerID=configPath.replace("/", "").lower())
            addToJS("for (element in data." + configPath.replace("/", ".") + ") { createNewTag(document.getElementById('tagsContainer-" + configPath.replace("/", "").lower() + "'), data." + configPath.replace("/", ".") + "[element]) }")
        elif isinstance(currentElement, bool):
            configPath = f"{str(category)}/{str(element)}"
            categoryResult += newBooleanContainer.format(title=formatTitle(element), toggleID=configPath.replace("/", "").lower(), config_path=configPath)
            addToJS("if (data." + configPath.replace("/", ".") + " == true) { document.getElementById('toggle-" + configPath.replace("/", "").lower() + "').checked = true; document.getElementById('toggleText-" + configPath.replace("/", "").lower() + "').innerText = 'Enabled' }")
        else:
            configPath = f"{str(category)}/{str(element)}"
            categoryResult += newTextContainer.format(title=formatTitle(element), config_path=configPath, inputID=configPath.replace("/", "").lower())
            addToJS("document.getElementById('" + configPath.replace("/", "").lower() + "').value = data." + configPath.replace("/", "."))

    if categoryResult != "":
        htmlResult += newCategory.format(expandableID=category.replace("/", "").lower(), categoryName=category, content=categoryResult)



htmlResult = htmlResult.replace("Tracemoe", "trace.moe").replace("Saucenao", "SauceNAO").replace("Iqdb", "IQDB")

htmlResult += """


<category-title>
    Information
</category-title>
<informations>
    <tenshi><img src="/erina/admin/static/images/Tenshi" alt="Tenshi: ErinaAdmin Logo" class="tenshi"></tenshi>
    <informations-container>
        <information info-type="Version"></information>
        <information info-type="Installed Dir"></information>
        <information info-type="Python Ver."></information>
        <information info-type="PID"></information>
        <information info-type="System"></information>
        <information>by Anime no Sekai © 2020</information>
    </informations-container>
</informations>

<category-title>
    System State
</category-title>
<states>
    <state state-type="CPU Count"></state>
    <state state-type="CPU Freq."></state>
    <state state-type="CPU Usage"></state>
    <state state-type="RAM Usage"><state-major id="ramUsed"></state-major>/<state-minor id="ramTotal"></state-minor>(<state-major id="ramPercent"></state-major>)</state>
    <state state-type="Disk Usage"><state-major id="diskUsed"></state-major>/<state-minor id="diskTotal"></state-minor>(<state-major id="diskPercent"></state-major>)</state>
    <state state-type="Disk Total Read"></state>
    <state state-type="Disk Total Write"></state>
    <state state-type="Net Total Sent"></state>
    <state state-type="Net Total Received"></state>
    <state state-type="Threads Count"></state>
</states>

<category-title>
    Actions
</category-title>

<actions>
    <action-button-container>
        <action-button id="resetErinaStats">Reset ErinaStats</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="resetLogs">Reset Logs</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="cleanCaches">Clean Caches</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="cleanDB">Clean ErinaDatabase</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="updateManami">Update Manami</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="revertConfig">Revert Config to default</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="updateErina">Update Erina</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="downloadBackup">Download Backup</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="importBackup">Import Backup</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="restartErinaServer">Restart ErinaServer</action-button>
    </action-button-container>
    <action-button-container>
        <action-button id="shutdownErinaServer">Shutdown ErinaServer</action-button>
    </action-button-container>
</actions>"""

print(htmlResult)
print("")
print("")
print("")
print("")
print("")
print("")
print(jsResult)