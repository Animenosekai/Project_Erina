
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

document.getElementById("cleanCaches").onclick = function() {
    if (confirm("Do you really want to clean all of the caches?") == true) {
        if (confirm("Do you want to delete AniList Caches?") == false) {
            fetch("/erina/api/admin/caches/clean?token=" + window.localStorage.getItem("erinaAdminToken"), {
                method: "POST"
            })
            .then((resp) => resp.json())
            .then(function(data) {
                if (data.success == true) {
                    newSuccess("Successfully cleaned ErinaCaches")
                } else {
                    newError("An error occured while cleaning the caches")
                }
            })
        } else {
            if (confirm("[Warning] AniList Caches Data is even more important because used by all of the ErinaSearch endpoints, make sure not to get rate limited\nDo you want to proceed?") == true) {
                fetch("/erina/api/admin/caches/clean?anilist=true&token=" + window.localStorage.getItem("erinaAdminToken"), {
                    method: "POST"
                })
                .then((resp) => resp.json())
                .then(function(data) {
                    if (data.success == true) {
                        newSuccess("Successfully cleaned ErinaCaches")
                    } else {
                        newError("An error occured while cleaning the caches")
                    }
                })
            }
        }
    }
}

document.getElementById("cleanDB").onclick = function() {
    if (confirm("Do you really want to clean all of the files in your ErinaDatabase?") == true) {
        fetch("/erina/api/admin/database/clean?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Successfully cleaned ErinaDatabase")
            } else {
                newError("An error occured while cleaning ErinaDatabase")
            }
        })
    }
}

document.getElementById("updateManami").onclick = function() {
    fetch("/erina/api/admin/database/updateManami?token=" + window.localStorage.getItem("erinaAdminToken"), {
        method: "POST"
    })
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.success == true) {
            newSuccess("Successfully updated ManamiDatabase: " + String(data.data.manami))
        } else {
            newError("An error occured while updating ManamiDatabase")
        }
    })
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
            intervalsRegistry.push(_erinaAliveInterval)
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
        intervalsRegistry.push(_erinaAliveInterval)
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
        intervalsRegistry.push(_erinaAliveInterval)
    }

    if (confirm("Do you really want to update Erina?\nErina will restart at the end of the backup which will lead to a down time.") == true) {
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
                                    newError("Update failed")
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
                    intervalsRegistry.push(_updateInterval)
                }
            } else {
                newError("An error occured while updating Erina")
            }
        })
    }
}

document.getElementById("downloadBackup").onclick = function() {

    if (confirm("Do you want to download a backup of the generated data?\nMake sure to have enough space on your hard drive before doing so.") == true) {
        fetch("/erina/api/admin/backup/request?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST"
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                data = data.data
                if (data.status == "BACKUP_STARTED" || data.status == "ALREADY_REQUESTED") {
                    if (data.status == "BACKUP_STARTED") {
                        newSuccess(data.message)
                    } else {
                        newInfo(data.message)
                    }
                    var lastStatus = ""
                    var _updateInterval = setInterval(function() {
                        fetch("/erina/api/admin/backup/status?token=" + window.localStorage.getItem("erinaAdminToken"))
                        .then((resp) => resp.json())
                        .then(function(data) {
                            if (data.success == true) {
                                data = data.data
                                if (data.status == "LAST_BACKUP_FAILED") {
                                    clearInterval(_updateInterval)
                                    newError("Failed to backup")
                                }
                                else if (data.status == "READY_FOR_DOWNLOAD") {
                                    clearInterval(_updateInterval)
                                    fetch("/erina/api/admin/backup/download?token=" + window.localStorage.getItem("erinaAdminToken"), {
                                        method: 'GET'
                                    })
                                    .then(function(response) {
                                        if (response.status == 200) {
                                            return response.blob()
                                        } else if (response.status == 204) {
                                            newError("Could not download the backup because it is not ready yet")
                                            return null
                                        } else {
                                            newError("An error occured while downloading the backup")
                                            return null
                                        }
                                    })
                                    .then(blob => {
                                        if (blob != null) {
                                            var url = window.URL.createObjectURL(blob);
                                            var a = document.createElement('a');
                                            a.href = url;
                                            a.download = "ErinaBackup.zip";
                                            document.body.appendChild(a); // firefox compatibility
                                            a.click();
                                            a.remove();
                                            clearInterval(_updateInterval)
                                        }
                                    });
                                }
                                else if (data.status != lastStatus){
                                    lastStatus = data.status
                                    newInfo(data.message)
                                }
                            } else {
                                newError("An error occured while retrieving the status of the backup")
                            }
                        })
                    }, 1000)
                    intervalsRegistry.push(_updateInterval)
                } else {
                    newError(data.message)
                }
            } else {
                newError("An error occured while updating Erina")
            }
        })
    }
}

const backupToBase64 = file => new Promise((resolve, reject) => {
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});

function _importBackup(event) {

    function verifyAfterDown() {
        var _erinaAliveInterval = setInterval(function() {
            fetch("/erina/alive")
            .then(function() {
                newSuccess("Import Complete!\nErina successfully imported new backup data!")
                clearInterval(_erinaAliveInterval)
            })
            .catch(function() {
                console.log("Waiting for ErinaServer")
            })
        }, 500)
        intervalsRegistry.push(_erinaAliveInterval)
    }

    var file = event.target.files[0];
    if (!file) {
        return;
    }
    backupToBase64(file)
    .then(function(base64) {
        document.getElementById("_ErinaBackupImport_FileInput").remove()
        var formData = new FormData();
        formData.append("backupBase64Data", base64)
        fetch("/erina/api/admin/backup/import?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST",
            body: formData
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                data = data.data
                if (data.status == "IMPORT_STARTED" || data.status == "ALREADY_REQUESTED") {
                    if (data.status == "IMPORT_STARTED") {
                        newSuccess(data.message)
                    } else {
                        newInfo(data.message)
                    }
                    var lastStatus = ""
                    var _updateInterval = setInterval(function() {
                        fetch("/erina/api/admin/import/status?token=" + window.localStorage.getItem("erinaAdminToken"))
                        .then((resp) => resp.json())
                        .then(function(data) {
                            if (data.success == true) {
                                data = data.data
                                if (data.status == "LAST_IMPORT_FAILED") {
                                    newError("Import Failed")
                                    clearInterval(_updateInterval)
                                }
                                else if (data.status != lastStatus){
                                    lastStatus = data.status
                                    newInfo(data.message)
                                }
                            } else {
                                newError("An error occured while retrieving the status of the backup")
                            }
                        })
                        .catch(function() {
                            verifyAfterDown()
                            clearInterval(_updateInterval)
                            newInfo("Import: Waiting for ErinaServer to be back...")
                        })
                    }, 1000)
                    intervalsRegistry.push(_updateInterval)
                } else {
                    newError(data.message)
                }
            } else {
                newError("An error occured while updating Erina")
            }
        })

    })
    
}

document.getElementById("importBackup").onclick = function() {

    if (confirm("Do you want to import a backup to Erina?\nMake sure to have enough space on your hard drive before doing so.\n") == true) {
        var newFile = document.createElement("input")
        newFile.setAttribute("type", "file")
        newFile.setAttribute("id", "_ErinaBackupImport_FileInput")
        newFile.setAttribute("accept", "application/zip,application/octet-stream,application/x-zip-compressed,multipart/x-zip,.zip,.erinazip")
        newFile.addEventListener("change", _importBackup, false)
        document.body.appendChild(newFile)
        newFile.click()
    }
}


document.getElementById("checkTweet").onclick = function() {
    var tweetInput = prompt("Enter the URL of the tweet you want to check")
    if (tweetInput != null) {
        var formData = new FormData();
        formData.append("tweet", tweetInput)
        fetch("/erina/api/admin/twitter/checkTweet?token=" + window.localStorage.getItem("erinaAdminToken"), {
            method: "POST",
            body: formData
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Checking tweet...")
            } else {
                newError(data.message)
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
                data = data.data
                textInputElement.value = String(data.value)
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
            data = data.data
            if (data.value == true) {
                checkboxElement.checked = true
                document.getElementById(checkboxElement.id.replace("toggle", "toggleText")).innerText = "Enabled";
            } else {
                checkboxElement.checked = false
                document.getElementById(checkboxElement.id.replace("toggle", "toggleText")).innerText = "Disabled";
            }
            newSuccess("Successfully edited " + data.path + " to " + String(data.value))
        } else if (data.error == "MISSING_CRITICAL_KEY"){
            data = data.data
            checkboxElement.checked = false
            document.getElementById(checkboxElement.id.replace("toggle", "toggleText")).innerText = "Disabled";
            newError("Could not run " + String(data.client) + " because the " + String(data.key) + " is missing.")
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
        if (data.Twitter.imagePreview == true) { document.getElementById('toggle-twitterimagepreview').checked = true; document.getElementById('toggleText-twitterimagepreview').innerText = 'Enabled' };
        if (data.Twitter.checkMentions == true) { document.getElementById('toggle-twittercheckmentions').checked = true; document.getElementById('toggleText-twittercheckmentions').innerText = 'Enabled' };
        if (data.Twitter.checkDM == true) { document.getElementById('toggle-twittercheckdm').checked = true; document.getElementById('toggleText-twittercheckdm').innerText = 'Enabled' };
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
        document.getElementById('cachesanilistexpiration').value = data.Caches.anilistExpiration;
        document.getElementById('cacheskeystracemoe').value = data.Caches.keys.tracemoe;
        document.getElementById('cacheskeyssaucenao').value = data.Caches.keys.saucenao;
        document.getElementById('hashalgorithm').value = data.Hash.algorithm;
        document.getElementById('searchthresholdserinasimilarity').value = data.Search.thresholds.erinaSimilarity;
        document.getElementById('searchthresholdstracemoesimilarity').value = data.Search.thresholds.tracemoeSimilarity;
        document.getElementById('searchthresholdssaucenaosimilarity').value = data.Search.thresholds.saucenaoSimilarity;
        document.getElementById('searchthresholdsiqdbsimilarity').value = data.Search.thresholds.iqdbSimilarity;
        document.getElementById('serverhost').value = data.Server.host;
        document.getElementById('serverport').value = data.Server.port;
        if (data.Server.publicAPI == true) { document.getElementById('toggle-serverpublicapi').checked = true; document.getElementById('toggleText-serverpublicapi').innerText = 'Enabled' };


        //////////////////
        } else if (data.error == "login") {
            window.location.assign("/erina/admin/login")
        } else {
            newError("An error occured while retrieving the configuration")
        }
    }) // end of then()

    fetch("/erina/api/admin/information?token=" + window.localStorage.getItem("erinaAdminToken"))
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.success == true) {
            data = data.data
            document.querySelector('information[info-type="Version"]').innerText = data.version
            document.querySelector('information[info-type="Installed Dir"]').innerText = data.installed_directory
            document.querySelector('information[info-type="Python Ver."]').innerText = data.python_version
            document.querySelector('information[info-type="PID"]').innerText = data.pid
            document.querySelector('information[info-type="System"]').innerText = data.system
        } else {
            newError("An error occured while retrieving information about Erina")
        }
    })

    var stateInterval = setInterval(function() {
        fetch("/erina/api/admin/state?token=" + window.localStorage.getItem("erinaAdminToken"))
        .then((resp) => resp.json())
    .then(function(data) {
        if (data.success == true) {
            data = data.data
            document.querySelector('state[state-type="CPU Count"]').innerText = data.cpu_count
            document.querySelector('state[state-type="CPU Freq."]').innerText = data.cpu_frequency
            document.querySelector('state[state-type="CPU Usage"]').innerText = data.cpu_usage
            document.getElementById("ramUsed").innerText = data.ram_usage_used
            document.getElementById("ramTotal").innerText = data.ram_usage_total
            document.getElementById("ramPercent").innerText = data.ram_usage_percentage
            document.getElementById("diskUsed").innerText = data.disk_usage_used
            document.getElementById("diskTotal").innerText = data.disk_usage_total
            document.getElementById("diskPercent").innerText = data.disk_usage_percentage
            document.querySelector('state[state-type="Disk Total Read"]').innerText = data.disk_total_read
            document.querySelector('state[state-type="Disk Total Write"]').innerText = data.disk_total_write
            document.querySelector('state[state-type="Net Total Sent"]').innerText = data.net_total_sent
            document.querySelector('state[state-type="Net Total Received"]').innerText = data.net_total_received
            document.querySelector('state[state-type="Threads Count"]').innerText = data.threads
            
            }
        })
    }, 1000)
    intervalsRegistry.push(stateInterval)
} // end of PageInitialize()



