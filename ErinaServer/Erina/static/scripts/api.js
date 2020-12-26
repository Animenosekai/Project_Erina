function PageInitialize() {

    // Adds to the DOM Tree
    function addAuthorization(name, key, ratelimit, usage) {
        var newAuthorizationElem = document.createElement("api-authorization");
        var newAuthContainerElem = document.createElement("api-authorization-container");
        newAuthContainerElem.setAttribute("authorization-name", String(name));
        newAuthContainerElem.setAttribute("authorization-key", String(key));
        var newAuthKeyElem = document.createElement("api-authorization-key");
        newAuthKeyElem.innerText = String(key);
        var newAuthRateLimitElem = document.createElement("api-authorization-ratelimit");
        newAuthRateLimitElem.innerText = String(ratelimit);
        var newAuthStatsLimitElem = document.createElement("api-authorization-stats");
        newAuthStatsLimitElem.innerText = String(usage);
        var newAuthRemoveElem = document.createElement("remove-auth");
        newAuthRemoveElem.innerText = "Remove Auth";
        newAuthRemoveElem.addEventListener("click", function() {
            removeAuth(String(key))
        })
        newAuthContainerElem.appendChild(newAuthKeyElem);
        newAuthContainerElem.appendChild(newAuthRateLimitElem);
        newAuthContainerElem.appendChild(newAuthStatsLimitElem);
        newAuthContainerElem.appendChild(newAuthRemoveElem);
        newAuthorizationElem.appendChild(newAuthContainerElem);
        document.getElementById("authorizationsList").appendChild(newAuthorizationElem);
    }

    // Sends to the server
    function newAuthorization() {
        var newAuthNameElem = document.getElementById("authorizationPopUp_name")
        var newAuthRateLimitElem = document.getElementById("authorizationPopUp_ratelimit")
        if (newAuthNameElem.value.replace(" ", "") != "" && String(newAuthRateLimitElem.value) != "") {
            var formData = new FormData();
            formData.append("name", newAuthNameElem.value)
            formData.append("ratelimit", newAuthRateLimitElem.value)
            fetch("/erina/api/admin/apiAuth/new?token=" + window.localStorage.getItem("erinaAdminToken"), {
                body: formData,
                method: "POST"
            })
            .then((resp) => resp.json())
            .then(function(data) {
                if (data.success == true) {
                    newSuccess("Successfully added a new API authorization")
                    var newAuth = data.data
                    addAuthorization(newAuth.name, newAuth.key, newAuth.rateLimit, newAuth.usage)
                    closeAuthPopUp()
                } else {
                    newError("An error occured while adding the new authorization")
                }
            })
        } else if (newAuthNameElem.value.replace(" ", "") == "") {
            newAuthNameElem.focus()
        } else {
            newAuthRateLimitElem.focus()
        }
    }

    function removeAuth(key) {
        fetch("/erina/api/admin/apiAuth/remove?token=" + window.localStorage.getItem("erinaAdminToken") + "&key=" + String(key), {
            method: "POST",
        })
        .then((resp) => resp.json())
        .then(function(data) {
            if (data.success == true) {
                newSuccess("Successfully removed an authorization")
                document.querySelector('api-authorization-container[authorization-key="' + String(key) + '"]').parentElement.remove()
            } else {
                newError("An error occured while removing an authorization")
            }
        })
    }

    function openAuthPopUp() {
        document.getElementById("authPopup").style.display = "flex"
        setTimeout(function() {
            document.getElementById("authPopup").classList.add("showPopup")
        }, 100)
    }

    function closeAuthPopUp() {
        document.getElementById("authPopup").classList.remove("showPopup")
        setTimeout(function() {
            document.getElementById("authPopup").style.display = "none"
        }, 1100)
    }

    /// EVENT LISTENERS

    document.getElementById("openAuthPopUp").addEventListener("click", openAuthPopUp)
    document.getElementById("closeAuthPopUp").addEventListener("click", closeAuthPopUp)
    document.getElementById("submitPopUp").addEventListener("click", newAuthorization)


    //TEST: addAuthorization("Anime no Sekai", "aaa0a0a0a0aaa0a0a0a0a0a0a", "1", "215")

    /// RETRIEVE EXISTING AUTHS

    fetch("/erina/api/admin/apiAuth?token=" + window.localStorage.getItem("erinaAdminToken"))
    .then((resp) => resp.json())
    .then(function(data) {
        if (data.success == true) {
            for (authorization in data.data) {
                var currentAuth = data.data[authorization]
                addAuthorization(currentAuth.name, currentAuth.key, currentAuth.rateLimit, currentAuth.usage)
            }
        } else {
            newError("An error occured while retrieving the API authorizations")
        }
    })
    
}