function PageInitialize() {

    function formatTime(dateObj) {
        const currentTime = new Date()
        if (dateObj.getDate() != currentTime.getDate()) {
            return String(dateObj.getDate()) + "/" + String(dateObj.getMonth())
        } else {
            //return String(dateObj.getHours()) + ":" + String(dateObj.getMinutes()) + ":" + String(dateObj.getSeconds())
            return String(dateObj.getHours()) + ":" + String(dateObj.getMinutes())
        }
    }

    fetch("/erina/api/stats")
    .then(function(data) {
        return data.json()
    })
    .then(function(data) {
        for (category in data) {
            try {
                if (category != "uptime") {
                    var currentCategory = data[category]
                    for (subcategory in currentCategory) {
                        try {
                            if (currentCategory[subcategory]["success"] == true) {
                                var closestTimestamp = 0
                                var results = []
                                for (timestamp in currentCategory[subcategory]["values"]) {
                                    if (closestTimestamp < timestamp) {
                                        closestTimestamp = timestamp
                                    }
                                    results.push({ "date": new Date(timestamp * 1000), "value": currentCategory[subcategory]["values"][timestamp]})
                                }
                                var currentID = "erinaStat-" + category + "-" + subcategory
                                document.getElementById(currentID + "-Value").innerText = currentCategory[subcategory]["values"][closestTimestamp]
                                createChart(currentID + "-Chart", results, am4core.color("#7ae2ff"))
                            }
                        } catch {
                            console.log("Error while adding subcategory: " + String(subcategory))
                        }
                    }
                } else {
                    document.getElementById("erinaStat-erina-uptime-Value").innerText = formatTime(new Date(data["uptime"] * 1000))
                }
            } catch {
                console.log("Error while adding category: " + String(category))
            }
        }
    })
}