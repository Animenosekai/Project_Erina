
function _hideSelectionLine(){
    document.getElementById("overviewSelectionLine").style.opacity = 0;
    document.getElementById("statsSelectionLine").style.opacity = 0;
    document.getElementById("apiSelectionLine").style.opacity = 0;
    document.getElementById("configSelectionLine").style.opacity = 0;
}


window.onload = function(){
    startLoading()
    var token = String(window.localStorage.getItem("erinaAdminToken"))
    const currentPage = window.location.pathname
    if (currentPage == "/erina/admin/overview") {
        goTo("Erina Admin — Overview", "overview")
    } else if (currentPage == "/erina/admin/stats") {
        goTo("Erina Admin — Stats", "stats")
    } else if (currentPage == "/erina/admin/api") {
        goTo("Erina Admin — API", "api")
    } else if (currentPage == "/erina/admin/config") {
        goTo("Erina Admin — Configuration", "config")
    } else {
        goTo("ErinaAdmin — Overview", "overview")
    }
    stopLoading()
}


function goTo(title, url, resourceLocation=null) {
    startLoading()
    title = String(title)
    url = String(url)
    if (resourceLocation == null) {
        resourceLocation = url
    } else {
        resourceLocation = String(resourceLocation)
    }
    const token = String(window.localStorage.getItem("erinaAdminToken"))
    if ("undefined" !== typeof history.pushState) {
        try {
            fetch("/erina/admin/resource/" + resourceLocation + "?token=" + token)
            .then(function(data){
                return data.text()
            })
            .then(function(data){
                if (data == "ErinaAdminLoginRedirect") {
                    window.location.assign("/erina/admin/login")
                }
                _hideSelectionLine()
                document.getElementById(url + "SelectionLine").style.opacity = 1;
                document.getElementById("ErinaAdminBody").innerHTML = data
                history.pushState({page: title}, title, "/erina/admin/" + url);
                stopLoading()
            })
        } catch {
            window.location.assign("/erina/admin/" + url)
        }
    } else {
      window.location.assign("/erina/admin/" + url);
    }
}