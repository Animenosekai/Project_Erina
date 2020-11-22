window.onload = function(){
    var token = String(window.localStorage.getItem("erinaAdminToken"))
    const currentPage = window.location.pathname
    if (currentPage == "/overview") {
        fetch("/erina/admin/resource/overview?token=" + String(token))
        .then(function(data){
            document.getElementById("ErinaAdminBody").innerHTML = data
        })
    } else if (currentPage == "/stats") {
        fetch("/erina/admin/resource/stats?token=" + String(token))
        .then(function(data){
            document.getElementById("ErinaAdminBody").innerHTML = data
        })
    } else if (currentPage == "/api") {
        fetch("/erina/admin/resource/api?token=" + String(token))
        .then(function(data){
            document.getElementById("ErinaAdminBody").innerHTML = data
        })
    } else if (currentPage == "/config") {
        fetch("/erina/admin/resource/config?token=" + String(token))
        .then(function(data){
            document.getElementById("ErinaAdminBody").innerHTML = data
        })
    } else {
        goTo("ErinaAdmin — Overview", "overview")
    }
}

function goTo(title, url, resourceLocation=null) {
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
            history.pushState({page: title}, title, "/erina/admin/" + url);
            fetch("/erina/admin/resource/" + resourceLocation + "?token=" + token)
            .then(function(data){
                document.getElementById("ErinaAdminBody").innerHTML = data
            })
        } catch {
            window.location.assign("/erina/admin/" + url)
        }
    } else {
      window.location.assign("/erina/admin/" + url);
    }
}