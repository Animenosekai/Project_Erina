var scriptsLoadingQueue = []
var chartsRegistry = []

function _hideSelectionLine(){
    document.getElementById("overviewSelectionLine").classList.remove("sidebarShow");
    document.getElementById("statsSelectionLine").classList.remove("sidebarShow");
    document.getElementById("apiSelectionLine").classList.remove("sidebarShow");
    document.getElementById("configSelectionLine").classList.remove("sidebarShow");
}

window.onload = function(){
    startLoading()
    const currentPage = window.location.pathname
    if (currentPage == "/erina/admin/overview") {
        goTo("ErinaAdmin", "overview")
    } else if (currentPage == "/erina/admin/stats") {
        goTo("ErinaAdmin — Stats", "stats")
    } else if (currentPage == "/erina/admin/api") {
        goTo("ErinaAdmin — API", "api")
    } else if (currentPage == "/erina/admin/config") {
        goTo("ErinaAdmin — Configuration", "config")
    } else {
        goTo("ErinaAdmin", "overview")
    }
    stopLoading()

    if (window.location.protocol == "https:") {
        ErinaLogsConnection = new WebSocket("wss://" + window.location.host + "/erina/websockets/Logs")
    } else {
        ErinaLogsConnection = new WebSocket("ws://" + window.location.host + "/erina/websockets/Logs")
    }
    ErinaLogsConnection.onopen = function() {
        ErinaLogsConnection.send(JSON.stringify({"token": window.localStorage.getItem("erinaAdminToken")}))
    }
    ErinaLogsConnection.onmessage = function(response){
        data = JSON.parse(response.data)
        if (data.error == true) {
            newError("[" + data.api + "] " + data.message)
        }
    }
}

function loadNextScript() {
    scriptsLoadingQueue.shift()
    if (scriptsLoadingQueue.length == 0) {
        PageInitialize()
        stopLoading()
    } else {
        var newScript = document.createElement("script");
        newScript.src = scriptsLoadingQueue[0]
        newScript.classList.add("ErinaExternalJS")
        newScript.addEventListener("load", loadNextScript)
        document.getElementsByTagName("head")[0].appendChild(newScript)
    }
}

function _goTo() {
    if ("undefined" !== typeof history.pushState) {
        try {
            var url = window.location.href.substring(window.location.href.lastIndexOf("/") + 1)
            fetch("/erina/admin/resource/" + url + "?token=" + window.localStorage.getItem("erinaAdminToken"))
            .then(function(data){
                return data.text()
            })
            .then(function(data){
                if (data == "ErinaAdminLoginRedirect") {
                    window.location.assign("/erina/admin/login")
                } else {
                    _hideSelectionLine()
                    document.getElementById(url + "SelectionLine").classList.add("sidebarShow");
                    for (chart in chartsRegistry) {
                        chartsRegistry[chart].dispose()
                    }
                    document.getElementById("ErinaAdminBody").innerHTML = data
                    
                    
                    scriptsLoadingQueue = JSON.parse(document.getElementById("ErinaExternalJS-Sources").innerText)
                    if (scriptsLoadingQueue.length == 0) {
                        stopLoading()
                    } else {
                        var newScript = document.createElement("script");
                        newScript.src = scriptsLoadingQueue[0]
                        newScript.classList.add("ErinaExternalJS")
                        newScript.addEventListener("load", loadNextScript)
                        document.getElementsByTagName("head")[0].appendChild(newScript)
                    }
                }
            })
        } catch {
            window.getElementById("ErinaAdminBody").innerHTML = "An error occured while loading the page"
        }
    } else {
        window.getElementById("ErinaAdminBody").innerHTML = "Please upgrade your browser"
    }
}

window.onpopstate = _goTo()

function goTo(title, url) {
    startLoading()
    if ("undefined" !== typeof history.pushState) {
        title = String(title)
        url = String(url)
        history.pushState({page: title}, title, "/erina/admin/" + url);
        document.title = title
        _goTo()
    } else {
        window.getElementById("ErinaAdminBody").innerHTML = "Please upgrade your browser"
        stopLoading()
    }
}


function logout() {
    fetch("/erina/auth/logout?token=" + window.localStorage.getItem("erinaAdminToken"), {method: "POST"})
    window.location.assign("/erina/admin/login")
}


function convert(value) {
    if ( value >= 1000000000 ) {
        value = (Math.round((value / 1000000000  + Number.EPSILON) * 100) / 100) + "B"
    } else if ( value >= 1000000 ) {
        value = (Math.round((value / 1000000 + Number.EPSILON) * 100) / 100) + "M"
    } else if ( value >= 1000 ) {
        value = (Math.round((value / 1000 + Number.EPSILON) * 100) / 100)+ "K";
    }
    return value;
}


function formatTime(dateObj) {
    const currentTime = new Date()
    if (dateObj.getDate() != currentTime.getDate()) {
        return String(dateObj.getDate()) + "/" + String(dateObj.getMonth())
    } else {
        //return String(dateObj.getHours()) + ":" + String(dateObj.getMinutes()) + ":" + String(dateObj.getSeconds())
        var minutes = String(dateObj.getMinutes())
        if (minutes.length < 2) {
            minutes = "0" + minutes
        }
        return String(dateObj.getHours()) + ":" + minutes
    }
}



/*********** INFO BOX */


var messagesQueue = []
var currentIndex = 1

/** **/

function newInfo(message) {
    console.log(message)
    messagesQueue.push(message)
    let currentLength = messagesQueue.length
    let intervalID = setInterval(function(){
        if (currentIndex == currentLength) {
            var newElement = document.createElement("p")
            newElement.setAttribute("class", "info")
            newElement.innerText = String(message)
            document.getElementsByTagName("body")[0].appendChild(newElement)
            setTimeout(function() {
                newElement.classList.add("show")
            }, 100)
            setTimeout(function (){
                newElement.classList.remove("show")
                currentIndex += 1
            }, 5100)
            clearInterval(intervalID)
        }
    }, 100)
}

function newSuccess(message) {
    console.log(message)
    messagesQueue.push(message)
    let currentLength = messagesQueue.length
    let intervalID = setInterval(function(){
        if (currentIndex == currentLength) {
            var newElement = document.createElement("p")
            newElement.setAttribute("class", "success")
            newElement.innerText = String(message)
            document.getElementsByTagName("body")[0].appendChild(newElement)
            setTimeout(function() {
                newElement.classList.add("show")
            }, 100)
            setTimeout(function (){
                newElement.classList.remove("show")
                currentIndex += 1
            }, 5100)
            clearInterval(intervalID)
        }
    }, 100)
}

function newError(message) {
    console.error(message)
    messagesQueue.push(message)
    let currentLength = messagesQueue.length
    let intervalID = setInterval(function(){
        if (currentIndex == currentLength) {
            var newElement = document.createElement("p")
            newElement.setAttribute("class", "error")
            newElement.innerText = String(message)
            document.getElementsByTagName("body")[0].appendChild(newElement)
            setTimeout(function() {
                newElement.classList.add("show")
            }, 100)
            setTimeout(function (){
                newElement.classList.remove("show")
                currentIndex += 1
            }, 5100)
            clearInterval(intervalID)
        }
    }, 100)
}


window.addEventListener('load', function(){
    newInfo("The page has been loaded")
})

window.addEventListener("online", function(){
    newInfo("You are back online")
})

window.addEventListener("offline", function(){
    newInfo("You seem to be disconnected")
})


function startLoading() {
    document.getElementById("loadingIndicator").style.display = "block"
}

function stopLoading() {
    document.getElementById("loadingIndicator").style.display = "none"
}