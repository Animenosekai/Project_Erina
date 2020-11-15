window.onload = function(){
    var WSConnection = new WebSocket("ws://127.0.0.1:5555/ErinaConsole")
    var History = []
    var HistoryIndex = 0
    WSConnection.onmessage = function(response){
        date = new Date();
        var hours = String(date.getHours());
        var minutes = String(date.getMinutes());
        var seconds = String(date.getSeconds());
        if (hours.length == 1) {
            hours = "0" + hours
        }
        if (minutes.length == 1) {
            minutes = "0" + minutes
        }
        if (seconds.length == 1) {
            seconds = "0" + seconds
        }
        dateString = hours + ":" + minutes + ":" + seconds
        data = JSON.parse(response.data)

        var newDateElement = document.createElement("timestamp")
        newDateElement.innerText = dateString
        var newMessage = document.createElement("outputdata")
        newMessage.innerText = data["message"]
        var newWrapper = document.createElement("output")
        newWrapper.appendChild(newDateElement)
        newWrapper.appendChild(newMessage)
        if (parseInt(data["code"]) != 0) {
            var newError = document.createElement("outputerror")
            newError.innerText = "ErinaConsole: [Error] Process returned " + String(data["code"])
            newWrapper.appendChild(newError)
        }
        document.getElementById("consoleOutput").appendChild(newWrapper)
        document.getElementById("consoleOutput").scrollTop = document.getElementById("consoleOutput").scrollHeight
    }
    function submitInput() {
        var userInput = document.getElementById("consoleInput").value;
        WSConnection.send(JSON.stringify({"input": userInput}))
        History.push(document.getElementById("consoleInput").value)
        HistoryIndex = History.length
        document.getElementById("consoleInput").value = ""
    }
    document.getElementById("consoleInput").addEventListener("keyup", function(e) {
        if (!e) {
            var e = window.event;
        }
        e.preventDefault()
        if (e.keyCode == 13) {
            submitInput()
        } else if (e.keyCode == 38) {
            //console.log("History Up!")
            HistoryIndex -= 1
            if (HistoryIndex < 0) {
                HistoryIndex = 0
            }
            document.getElementById("consoleInput").value = History[HistoryIndex]
        } else if (e.keyCode == 40) {
            //console.log("History Down!")
            HistoryIndex += 1
            if (HistoryIndex > History.length - 1) {
                HistoryIndex = History.length
                document.getElementById("consoleInput").value = ''
            } else {
            document.getElementById("consoleInput").value = History[HistoryIndex]
            }
        }
    })





    //Make the DIV element draggagle:
    dragElement(document.getElementById("console"));

    function dragElement(elmnt) {
        var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
        if (document.getElementById(elmnt.id + "Header")) {
            /* if present, the header is where you move the DIV from:*/
            document.getElementById(elmnt.id + "Header").onmousedown = dragMouseDown;
        } else {
            /* otherwise, move the DIV from anywhere inside the DIV:*/
            elmnt.onmousedown = dragMouseDown;
        }

        function dragMouseDown(e) {
            e = e || window.event;
            e.preventDefault();
            // get the mouse cursor position at startup:
            pos3 = e.clientX;
            pos4 = e.clientY;
            document.onmouseup = closeDragElement;
            // call a function whenever the cursor moves:
            document.onmousemove = elementDrag;
        }

        function elementDrag(e) {
            e = e || window.event;
            e.preventDefault();
            // calculate the new cursor position:
            pos1 = pos3 - e.clientX;
            pos2 = pos4 - e.clientY;
            pos3 = e.clientX;
            pos4 = e.clientY;
            // set the element's new position:
            elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
            elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        }

        function closeDragElement() {
            /* stop moving when mouse button is released:*/
            document.onmouseup = null;
            document.onmousemove = null;
        }
    }
}