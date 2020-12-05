function PageInitialize() {
    function addTag(tagContainer, value, update=false) {
        var tags = []
        var childElements = tagContainer.children;
        for (var i = 0; i < childElements.length; i++) {
            if (childElements.item(i).innerText == value) {
                return
            } else {
                tags.push(childElements.item(i).innerText)
            }
        }
        tags.push(value)
        
        const configPath = tagContainer.getAttribute("config-path")
        if (update == true) {
            var formData = new FormData();
            formData.append("path", configPath)
            formData.append("value", tags)
            fetch("/erina/api/admin/config/update", {
                body: formData,
                method: "POST"
            })
        }

        var newTag = document.createElement("a")
        newTag.classList.add("tag")
        newTag.innerText = value
        var newCross = document.createElement("span")
        newCross.innerText = "X"
        newCross.classList.add("tagCross")
        newCross.onclick = "removeTag(this, '" + configPath + "')"
        newTag.appendChild(newCross)
        tagContainer.appendChild(newTag)
    }

    function removeTag(tagElement) {
        var container = tagElement.parentElement()
        tagElement.remove()
        var tags = [];
        for (var i = 0; i < container.children.length; i++) {
            tags.push(container.children.item(i).innerText)
        }
        var formData = new FormData();
        formData.append("path", container.getAttribute("config-path"))
        formData.append("value", tags)
        fetch("/erina/api/admin/config/update", {
            body: formData,
            method: "POST"
        })
    }

    function tagInputCallback(event, inputElement) {
        if (event.which == 13) {
            console.log("Tag Enter")
            const container = inputElement.nextElementSibling;
            const value = inputElement.value
            addTag(container, value, true)
        }
        return
    }


    function checkboxHandler(checkboxElement) {
        console.log("Checkbox")
        var formData = new FormData();
        formData.append("path", checkboxElement.getAttribute("config-path"))
        formData.append("value", checkboxElement.checked)
        fetch("/erina/api/admin/config/update", {
            body: formData,
            method: "POST"
        })
    }

    fetch("/erina/api/admin/config/get")
    .then((resp) => resp.json())
    .then(function(data){
///////////////////// PASTING JS MADE WITH CONFIGPAGESETUP.PY


        for (element in data.Erina.flags) { addTag(document.getElementById('tagsContainer-erinaflags'), data.Erina.flags.element) };
        if (data.Erina.consoleLog == true) { document.getElementById('toggle-erinaconsolelog').checked = true; document.getElementById('toggleText-erinaconsolelog').innerText = 'Enabled' } else { console.log('Not enabled') };
        if (data.Erina.fileLog == true) { document.getElementById('toggle-erinafilelog').checked = true; document.getElementById('toggleText-erinafilelog').innerText = 'Enabled' } else { console.log('Not enabled') };
        if (data.Erina.stats == true) { document.getElementById('toggle-erinastats').checked = true; document.getElementById('toggleText-erinastats').innerText = 'Enabled' } else { console.log('Not enabled') };
        if (data.Twitter.run == true) { document.getElementById('toggle-twitterrun').checked = true; document.getElementById('toggleText-twitterrun').innerText = 'Enabled' } else { console.log('Not enabled') };
        for (element in data.Twitter.ignoredUsers) { addTag(document.getElementById('tagsContainer-twitterignoredusers'), data.Twitter.ignoredUsers.element) };
        for (element in data.Twitter.flags) { addTag(document.getElementById('tagsContainer-twitterflags'), data.Twitter.flags.element) };
        if (data.Twitter.ignoreRT == true) { document.getElementById('toggle-twitterignorert').checked = true; document.getElementById('toggleText-twitterignorert').innerText = 'Enabled' } else { console.log('Not enabled') };
        document.getElementById('twitterkeysconsumerkey').value = data.Twitter.keys.consumerKey;
        document.getElementById('twitterkeysconsumersecret').value = data.Twitter.keys.consumerSecret;
        document.getElementById('twitterkeysaccesstokenkey').value = data.Twitter.keys.accessTokenKey;
        document.getElementById('twitterkeysaccesstokensecret').value = data.Twitter.keys.accessTokenSecret;
        for (element in data.Twitter.stream.languages) { addTag(document.getElementById('tagsContainer-twitterstreamlanguages'), data.Twitter.stream.languages.element) };
        for (element in data.Twitter.stream.flags) { addTag(document.getElementById('tagsContainer-twitterstreamflags'), data.Twitter.stream.flags.element) };
        for (element in data.Twitter.monitoring.accounts) { addTag(document.getElementById('tagsContainer-twittermonitoringaccounts'), data.Twitter.monitoring.accounts.element) };
        if (data.Twitter.monitoring.checkReplies == true) { document.getElementById('toggle-twittermonitoringcheckreplies').checked = true; document.getElementById('toggleText-twittermonitoringcheckreplies').innerText = 'Enabled' } else { console.log('Not enabled') };
        if (data.Discord.run == true) { document.getElementById('toggle-discordrun').checked = true; document.getElementById('toggleText-discordrun').innerText = 'Enabled' } else { console.log('Not enabled') };
        for (element in data.Discord.flags) { addTag(document.getElementById('tagsContainer-discordflags'), data.Discord.flags.element) };
        document.getElementById('discordkeystoken').value = data.Discord.keys.token;
        if (data.Line.run == true) { document.getElementById('toggle-linerun').checked = true; document.getElementById('toggleText-linerun').innerText = 'Enabled' } else { console.log('Not enabled') };
        for (element in data.Line.flags) { addTag(document.getElementById('tagsContainer-lineflags'), data.Line.flags.element) };
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
        if (data.Server.disableConsoleMessages == true) { document.getElementById('toggle-serverdisableconsolemessages').checked = true; document.getElementById('toggleText-serverdisableconsolemessages').innerText = 'Enabled' } else { console.log('Not enabled') };


//////////////////
    })

}