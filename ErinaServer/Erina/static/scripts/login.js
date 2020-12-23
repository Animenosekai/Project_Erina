window.onload = function() {
    fetch("/erina/auth/verify") 
    .then((resp) => resp.json())
    .then(function(data){
        if (data.error == "NOT_SET_PASSWORD") {
            setPage()
            document.getElementById("goToLogin").remove()
            document.getElementById("loginPage").remove()
            document.getElementsByClassName("fixedButtonContainer")[0].style.left = "44%"
        } else {
            loginPage()
        }
    })
}

function loginInputCallback(event) {
    if (event.key == "Enter" && String(document.getElementById("passwordInput").value).replace(" ", "") != "") {
        login()
    }
}

function setTempInputCallback(event) {
    if (event.key == "Enter" && String(document.getElementById("tempCodeInput").value).replace(" ", "") != "") {
        if (String(document.getElementById("newPasswordInput").value).replace(" ", "") != "") {
            setPassword()
        } else {
            document.getElementById("newPasswordInput").focus()
        }
    }
}

function setPasswordInputCallback(event) {
    if (event.key == "Enter" && String(document.getElementById("newPasswordInput").value).replace(" ", "") != "") {
        if (String(document.getElementById("tempCodeInput").value).replace(" ", "") != "") {
            setPassword()
        } else {
            document.getElementById("tempCodeInput").focus()
        }
    }
}

function setPage() {
    fetch("/erina/auth/displayCode")
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            newInfo("A temp code is displayed on your console")
        } else {
            newError("An error occured while displaying your temp code")
        }
    })
    document.getElementById("loginPage").classList.add("hidden")
    document.getElementById("setPage").classList.remove("hidden")
}

function loginPage() {
    document.getElementById("setPage").classList.add("hidden")
    document.getElementById("loginPage").classList.remove("hidden")
}


function login() {
    document.getElementById("passwordInput").blur()
    var formData = new FormData();
    formData.append("password", document.getElementById("passwordInput").value)
    fetch("/erina/auth/login", {
        body: formData,
        method: "POST"
    })
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            window.localStorage.setItem("erinaAdminToken", data.data.token)
            newSuccess("Successfully logged in!")
            window.location.assign("/erina/admin/overview")
        } else if (data.error == "WRONG_PASSWORD") {
            document.getElementById("passwordInput").value = ""
            newError("Wrong Password")
        } else {
            document.getElementById("passwordInput").focus()
            newError("An error occured while logging you in")
        }
    })
}

function setPassword() {
    document.getElementById("tempCodeInput").blur()
    document.getElementById("newPasswordInput").blur()
    
    var formData = new FormData();
    formData.append("password", document.getElementById("newPasswordInput").value)
    formData.append("tempCode", document.getElementById("tempCodeInput").value)
    
    fetch("/erina/auth/set", {
        body: formData,
        method: "POST"
    })
    .then((resp) => resp.json())
    .then(function(data){
        if (data.success == true) {
            window.localStorage.setItem("erinaAdminToken", data.data.token)
            newSuccess("Successfully logged in!")
            window.location.assign("/erina/admin/overview")
        } else if (data.error == "WRONG_TEMPCODE") {
            document.getElementById("tempCodeInput").value = ""
            document.getElementById("tempCodeInput").focus()
            newError("This is the wrong temp code\nCheck the temp code on your server's console")
        } else {
            newError("An error occured while setting the password")
        }
    })
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
