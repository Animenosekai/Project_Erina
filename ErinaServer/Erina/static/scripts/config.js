
/////// ACTIONS

document.getElementById("resetErinaStats").onclick = function() {
    if (confirm("Do you really want to reset ErinaStats?") == true) {
        fetch("/erina/api/admin/stats/reset?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Successfully resetted ErinaStats")
            } else {
                newError("An error occured while resetting ErinaStats")
            }
        })
    }
}

document.getElementById("resetLogs").onclick = function() {
    if (confirm("Do you really want to reset ErinaLogs?") == true) {
        fetch("/erina/api/admin/logs/reset?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Successfully resetted ErinaLogs")
            } else {
                newError("An error occured while resetting ErinaLogs")
            }
        })
    }
}

document.getElementById("revertConfig").onclick = function() {
    if (confirm("Do you really want to revert ErinaConfig to its default values?") == true) {
        fetch("/erina/api/admin/config/default?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Successfully reverted ErinaConfig")
            } else {
                newError("An error occured while reverting ErinaConfig to its default values")
            }
        })
    }
}

document.getElementById("restartErinaServer").onclick = function() {
    if (confirm("Do you really want to restart Erina?\nIt might take time to reinitialize everything and all of the clients will be down for a moment.") == true) {
        fetch("/erina/api/admin/restart?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Restarting Erina...")
            } else {
                newError("An error occured while restarting Erina")
            }
        })

        function verifyAfterDown() {
            var _erinaAliveInterval = setInterval(function() {
                fetch("/erina/alive")
                .then(function() {
                    newSuccess("Erina is back!")
                    clearInterval(_erinaAliveInterval)
                })
                .catch(function() {
                    console.log("Waiting for ErinaServer")
                })
            }, 500)
        }

        erinaIsOffline = false
        var _erinaAliveInterval = setInterval(function() {
            fetch("/erina/alive")
            .catch(function() {
                verifyAfterDown()
                clearInterval(_erinaAliveInterval)
                console.log("Waiting for ErinaServer")
            })
        }, 1000)
    }
}

document.getElementById("shutdownErinaServer").onclick = function() {
    if (confirm("Do you really want to shutdown Erina?\nAll of the clients will be down and you won't be able to access this page until you manually turn it back on.\nPlease also note that it will only exit Erina's process.") == true) {
        fetch("/erina/api/admin/shutdown?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Shutting down Erina...")
            } else {
                newError("An error occured while shutting down Erina")
            }
        })
    }
}

document.getElementById("updateErina").onclick = function() {

    function verifyAfterDown() {
        var _erinaAliveInterval = setInterval(function() {
            fetch("/erina/alive")
            .then(function() {
                newSuccess("Update Complete!\nErina got successfully updated!")
                clearInterval(_erinaAliveInterval)
            })
            .catch(function() {
                console.log("Waiting for ErinaServer")
            })
        }, 500)
    }

    if (confirm("Do you really want to update Erina?\nMake sure to add to the backup list all of the files you want to keep (other than the ones automatically backed up)\nErina will restart at the end of the backup which will lead to a down time.") == true) {
        fetch("/erina/api/admin/update?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                data = data.data
                newSuccess(data.message)
                if (data.status == "UPDATE_STARTED") {
                    var lastStatus = ""
                    var _updateInterval = setInterval(function() {
                        fetch("/erina/api/admin/update/status?token=" + window.localStorage.getItem("erinaAdminToken"))
                        .then((resp) => resp.json())
                        .then(function(data) {
                            if (data.success == true) {
                                data = data.data
                                if (data.status == "LAST_UPDATE_FAILED") {
                                    clearInterval(_updateInterval)
                                }
                                else if (data.status != lastStatus){
                                    lastStatus = data.status
                                    newInfo(data.message)
                                }
                            } else {
                                newError("An error occured while retrieving the status of the update")
                            }
                        })
                        .catch(function() {
                            verifyAfterDown()
                            clearInterval(_updateInterval)
                            newInfo("Update: Waiting for ErinaServer to be back...")
                        })
                    }, 1000)
                }
            } else {
                newError("An error occured while updating Erina")
            }
        })
    }
}

/////// TAGS

function updateTags(container) {
    var tags = "";
    for (var i = 0; i < container.querySelectorAll("span").length; i++) {
        if (tags != "") {
            tags = tags + ":::" + container.querySelectorAll("span")[i].innerText;
        } else {
            tags = container.querySelectorAll("span")[i].innerText;
        }
    }
    var formData = new FormData();
    formData.append("path", container.getAttribute("config-path"))
    formData.append("value", tags)
    fetch("/erina/api/admin/config/update?token=" + window.localStorage.getItem("erinaAdminToken"), {
        body: formData,
        method: "POST"
    })
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            newSuccess("Successfully edited " + container.getAttribute("config-path"))
        } else {
            newError("An error occured while editing " + container.getAttribute("config-path"))
        }
    })
}

function createNewTag(container, value) {

    const newDiv = document.createElement('div');
    newDiv.setAttribute('class', 'tag');
    const newSpan = document.createElement('span');
    newSpan.innerText = value;
    const closeIcon = document.createElement('i');
    closeIcon.innerHTML = 'close';
    closeIcon.setAttribute('class', 'material-icons');
    closeIcon.setAttribute('data-item', value);
    closeIcon.setAttribute("onclick", "removeTag(this)");
    newDiv.appendChild(newSpan);
    newDiv.appendChild(closeIcon);

    container.insertBefore(newDiv, container.querySelector("input"));
}

function addTag(input) {
    const value = input.value;
    const tagContainer = input.parentElement;
    var tags = [];
    var childElements = tagContainer.children;
    for (var i = 0; i < childElements.length; i++) {
        if (childElements.item(i).innerText == value) {
            return
        } else {
            tags.push(childElements.item(i).innerText);
        }
    }
    tags.push(value);

    const newDiv = document.createElement('div');
    newDiv.setAttribute('class', 'tag');
    const newSpan = document.createElement('span');
    newSpan.innerText = value;
    const closeIcon = document.createElement('i');
    closeIcon.innerHTML = 'close';
    closeIcon.setAttribute('class', 'material-icons');
    closeIcon.setAttribute('data-item', value);
    closeIcon.setAttribute("onclick", "removeTag(this)");
    newDiv.appendChild(newSpan);
    newDiv.appendChild(closeIcon);

    tagContainer.insertBefore(newDiv, input);

    updateTags(tagContainer);

    input.value = "";
}

function removeTag(tag) {
    const container = tag.parentElement.parentElement
    tag.parentElement.remove()
    updateTags(container)
}

function tagInputCallback(event, inputElement) {
    if (event.key == "Enter") {
        addTag(inputElement)
    }
    return
}



///// TEXT INPUT

function textInputHandler(event, textInputElement) {
    if (event.key == "Enter") {
        var formData = new FormData();
        formData.append("path", textInputElement.getAttribute("config-path"))
        formData.append("value", textInputElement.value)
        fetch("/erina/api/admin/config/update?token=" + window.localStorage.getItem("erinaAdminToken"), {
            body: formData,
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data){
            if (data.success == true) {
                newSuccess("Successfully edited " + data.path + " to " + String(data.value))
            } else {
                newError("An error occured while editing " + textInputElement.getAttribute("config-path"))
            }
        })
        textInputElement.blur()
    }
}


////// CHECKBOX

function checkboxHandler(checkboxElement) {
    var formData = new FormData();
    formData.append("path", checkboxElement.getAttribute("config-path"))
    formData.append("value", checkboxElement.checked)
    fetch("/erina/api/admin/config/update?token=" + window.localStorage.getItem("erinaAdminToken"), {
        body: formData,
        method: "POST"
    })
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            newSuccess("Successfully edited " + data.path + " to " + String(data.value))
        } else {
            newError("An error occured while editing " + checkboxElement.getAttribute("config-path"))
        }
    })
    if (checkboxElement.checked == true) {
        document.getElementById(checkboxElement.id.replace("toggle", "toggleText")).innerText = "Enabled";
    } else {
        document.getElementById(checkboxElement.id.replace("toggle", "toggleText")).innerText = "Disabled";
    }
}


function PageInitialize() {
    fetch("/erina/api/admin/config?token=" + window.localStorage.getItem("erinaAdminToken"))
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            data = data.data
///////////////////// PASTING JS MADE WITH CONFIGPAGESETUP.PY


        for (element in data.Erina.flags) { createNewTag(document.getElementById('tagsContainer-erinaflags'), data.Erina.flags[element]) };
        if (data.Erina.consoleLog == true) { document.getElementById('toggle-erinaconsolelog').checked = true; document.getElementById('toggleText-erinaconsolelog').innerText = 'Enabled' };
        if (data.Erina.fileLog == true) { document.getElementById('toggle-erinafilelog').checked = true; document.getElementById('toggleText-erinafilelog').innerText = 'Enabled' };
        if (data.Erina.stats == true) { document.getElementById('toggle-erinastats').checked = true; document.getElementById('toggleText-erinastats').innerText = 'Enabled' };
        document.getElementById('erinalogstimeout').value = data.Erina.logsTimeout;
        if (data.Twitter.run == true) { document.getElementById('toggle-twitterrun').checked = true; document.getElementById('toggleText-twitterrun').innerText = 'Enabled' };
        for (element in data.Twitter.ignoredUsers) { createNewTag(document.getElementById('tagsContainer-twitterignoredusers'), data.Twitter.ignoredUsers[element]) };
        for (element in data.Twitter.flags) { createNewTag(document.getElementById('tagsContainer-twitterflags'), data.Twitter.flags[element]) };
        if (data.Twitter.ignoreRT == true) { document.getElementById('toggle-twitterignorert').checked = true; document.getElementById('toggleText-twitterignorert').innerText = 'Enabled' };
        document.getElementById('twitterkeysconsumerkey').value = data.Twitter.keys.consumerKey;
        document.getElementById('twitterkeysconsumersecret').value = data.Twitter.keys.consumerSecret;
        document.getElementById('twitterkeysaccesstokenkey').value = data.Twitter.keys.accessTokenKey;
        document.getElementById('twitterkeysaccesstokensecret').value = data.Twitter.keys.accessTokenSecret;
        for (element in data.Twitter.stream.languages) { createNewTag(document.getElementById('tagsContainer-twitterstreamlanguages'), data.Twitter.stream.languages[element]) };
        for (element in data.Twitter.stream.flags) { createNewTag(document.getElementById('tagsContainer-twitterstreamflags'), data.Twitter.stream.flags[element]) };
        for (element in data.Twitter.monitoring.accounts) { createNewTag(document.getElementById('tagsContainer-twittermonitoringaccounts'), data.Twitter.monitoring.accounts[element]) };
        if (data.Twitter.monitoring.checkReplies == true) { document.getElementById('toggle-twittermonitoringcheckreplies').checked = true; document.getElementById('toggleText-twittermonitoringcheckreplies').innerText = 'Enabled' };
        if (data.Discord.run == true) { document.getElementById('toggle-discordrun').checked = true; document.getElementById('toggleText-discordrun').innerText = 'Enabled' };
        for (element in data.Discord.flags) { createNewTag(document.getElementById('tagsContainer-discordflags'), data.Discord.flags[element]) };
        document.getElementById('discordkeystoken').value = data.Discord.keys.token;
        if (data.Line.run == true) { document.getElementById('toggle-linerun').checked = true; document.getElementById('toggleText-linerun').innerText = 'Enabled' };
        for (element in data.Line.flags) { createNewTag(document.getElementById('tagsContainer-lineflags'), data.Line.flags[element]) };
        document.getElementById('linekeyschannelaccesstoken').value = data.Line.keys.channelAccessToken;
        document.getElementById('linekeyschannelsecret').value = data.Line.keys.channelSecret;
        document.getElementById('lineimagestimeout').value = data.Line.imagesTimeout;
        document.getElementById('cachesencoding').value = data.Caches.encoding;
        document.getElementById('cacheskeystracemoe').value = data.Caches.keys.tracemoe;
        document.getElementById('cacheskeyssaucenao').value = data.Caches.keys.saucenao;
        document.getElementById('hashalgorithm').value = data.Hash.algorithm;
        document.getElementById('searchthresholdserinasimilarity').value = data.Search.thresholds.erinaSimilarity;
        document.getElementById('searchthresholdstracemoesimilarity').value = data.Search.thresholds.tracemoeSimilarity;
        document.getElementById('searchthresholdssaucenaosimilarity').value = data.Search.thresholds.saucenaoSimilarity;
        document.getElementById('searchthresholdsiqdbsimilarity').value = data.Search.thresholds.iqdbSimilarity;
        document.getElementById('serverhost').value = data.Server.host;
        document.getElementById('serverport').value = data.Server.port;
        if (data.Server.disableConsoleMessages == true) { document.getElementById('toggle-serverdisableconsolemessages').checked = true; document.getElementById('toggleText-serverdisableconsolemessages').innerText = 'Enabled' };
                
                
        //////////////////
        } else if (data.error == "login") {
            window.location.assign("/erina/admin/login")
        } else {
            newError("An error occured while retrieving the configuration")
        }
    }) // end of then()
} // end of PageInitialize()



