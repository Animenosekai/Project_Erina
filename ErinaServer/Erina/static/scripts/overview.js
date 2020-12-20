function PageInitialize(){
    fetch("/erina/api/admin/stats")
    .then((resp) => resp.json())
    .then(function(data){
        if (data.search.searchCount.success == true) {
            var closestTimestamp = 0
            var results = []
            for (timestamp in data.search.searchCount.values) {
                if (closestTimestamp < timestamp) {
                    closestTimestamp = timestamp
                }
                results.push({ "date": new Date(timestamp * 1000), "value": data.search.searchCount.values[timestamp]})
            }
            document.getElementById("erinaStats-current-number-animesearch").innerText = data.search.searchCount.values[closestTimestamp]
            createChart("erinaChart-animesearch", results, am4core.color("#7ae2ff"))
        }
        
        if (data.twitter.responses.success == true) {
            var closestTimestamp = 0
            var results = []
            for (timestamp in data.twitter.responses.values) {
                if (closestTimestamp < timestamp) {
                    closestTimestamp = timestamp
                }
                results.push({ "date": new Date(timestamp * 1000), "value": data.twitter.responses.values[timestamp]})
            }
            document.getElementById("erinaStats-current-number-tweets").innerText = data.twitter.responses.values[closestTimestamp]
            createChart("erinaChart-tweets", results, am4core.color("#7ae2ff"))
        }
    })

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

    fetch("/erina/api/admin/logs")
    .then((resp) => resp.json())
    .then(function(data){
        for (element in data) {
            for (timestamp in data[element]) {
                addErinaLogs(timestamp, "info", data[element][timestamp])
            }
        }
    })

    fetch("/erina/api/admin/stats/biggestUsers")
    .then((resp) => resp.json())
    .then(function(data) {
        var finalRankString = ""
        if (data.length >= 1) {
            var keys = Object.keys(data[0])
            if (keys.length >= 1) {
                finalRankString = keys[0]
            } else {
                finalRankString = "No data"
            }
        } else {
            finalRankString = "No data"
        }
        document.getElementById("erinaWidget-bestuser-value").innerText = finalRankString
        
    })

    fetch("/erina/api/admin/stats/pastMonthErrors")
    .then((resp) => resp.json())
    .then(function(data) {
        document.getElementById("erinaWidget-errors-value").innerText = String(data.length)
    })
}

