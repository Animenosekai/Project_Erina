function PageInitialize(){
    console.log("Hello")
    const templateData = [
        { "date": new Date(2018, 0, 1, 8, 0, 0), "value": 57 },
        { "date": new Date(2018, 0, 1, 9, 0, 0), "value": 27 },
        { "date": new Date(2018, 0, 1, 10, 0, 0), "value": 24 },
        { "date": new Date(2018, 0, 1, 11, 0, 0), "value": 59 },
        { "date": new Date(2018, 0, 1, 12, 0, 0), "value": 33 },
        { "date": new Date(2018, 0, 1, 13, 0, 0), "value": 46 },
        { "date": new Date(2018, 0, 1, 14, 0, 0), "value": 20 },
        { "date": new Date(2018, 0, 1, 15, 0, 0), "value": 42 },
        { "date": new Date(2018, 0, 1, 16, 0, 0), "value": 59, "opacity": .9}
    ]

    createChart("erinaChart-animesearch", templateData, am4core.color("#7ae2ff"))
    createChart("erinaChart-tweets", templateData, am4core.color("#7ae2ff"))

    function formatTime(dateObj) {
        const currentTime = new Date()
        if (dateObj.getDate() != currentTime.getDate()) {
            return String(dateObj.getDate()) + "/" + String(dateObj.getMonth())
        } else {
            //return String(dateObj.getHours()) + ":" + String(dateObj.getMinutes()) + ":" + String(dateObj.getSeconds())
            return String(dateObj.getHours()) + ":" + String(dateObj.getMinutes())
        }
    }

    function addErinaLogs(timestamp, type, message) {
        var newLog = document.createElement("erinalog")
        var newTimestamp = document.createElement("erinalog-timestamp")
        newTimestamp.innerText = formatTime(new Date(timestamp * 1000))
        var newType = document.createElement("erinalog-type")
        newType.classList.add("erinaLogType-" + String(type).toLowerCase())
        var newLogMessage = document.createElement("erinalog-message")
        newLogMessage.innerText = String(message)
        newLog.appendChild(newTimestamp)
        newLog.appendChild(newType)
        newLog.appendChild(newLogMessage)
        var logsContainer = document.getElementById("erinalogs-container")
        if (logsContainer.childElementCount == 0) {
            logsContainer.appendChild(newLog)
        } else {
            logsContainer.insertBefore(newLog, logsContainer.firstChild)
        }
    }

    addErinaLogs(1606308945, "error", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606308945, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606308945, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606308945, "error", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606308945, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606308945, "error", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606311650, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606312050, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606312150, "error", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")
    addErinaLogs(1606312161, "info", "[ErinaAdmin] Testing ErinaLogs for ErinaAdmin")

}

