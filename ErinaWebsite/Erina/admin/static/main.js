window.onload = function(){
    window.location.pathname
}

function goTo(title, url, resourceLocation) {
    if ("undefined" !== typeof history.pushState) {
        try {
            history.pushState({page: title}, title, url);
            fetch(resourceLocation)
            .then(function(data){
                document.getElementById("ErinaAdminBody").innerHTML = data
            })
        } catch {
            window.location.assign(url)
        }
    } else {
      window.location.assign(url);
    }
}