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

    async function addStatsData(currentCategory, category, subcategory) {
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
                document.getElementById(currentID + "-Value").innerText = convert(currentCategory[subcategory]["values"][closestTimestamp])
                createChart(currentID + "-Chart", results, am4core.color("#7ae2ff"))
            }
        } catch {
            console.log("Error while adding subcategory: " + String(subcategory))
        }
    }

    fetch("/erina/api/admin/stats")
    .then(function(data) {
        return data.json()
    })
    .then(function(data) {
        for (category in data) {
            try {
                if (category != "uptime" && category != "animeSearchRank") {
                    var currentCategory = data[category]
                    for (subcategory in currentCategory) {
                        addStatsData(currentCategory, category, subcategory)
                    }
                } else if (category == "uptime") {
                    document.getElementById("erinaStat-erina-uptime-Value").innerText = formatTime(new Date(data["uptime"] * 1000))
                } else {
                    var finalRankString = ""
                    if (data["animeSearchRank"].length >= 3) {
                        finalRankString = Object.keys(data["animeSearchRank"][0])[0] + ", " + Object.keys(data["animeSearchRank"][1])[0] + ", " + Object.keys(data["animeSearchRank"][2])[0]
                    } else if (data["animeSearchRank"].length == 2) {
                        finalRankString = Object.keys(data["animeSearchRank"][0])[0] + ", " + Object.keys(data["animeSearchRank"][1])[0]
                    } else if (data["animeSearchRank"].length == 1) {
                        finalRankString = Object.keys(data["animeSearchRank"][0])[0]
                    } else {
                        finalRankString = "No data"
                    }
                    document.getElementById("erinaStat-search-animeRank-Value").innerText = finalRankString
                }
            } catch {
                console.log("Error while adding category: " + String(category))
            }
        }
    })
}