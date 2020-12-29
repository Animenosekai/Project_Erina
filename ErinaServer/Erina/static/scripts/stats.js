function PageInitialize() {

    async function addStatsData(currentCategory, category, subcategory) {
        try {
            if (currentCategory[subcategory]["success"] == true) {
                var closestTimestamp = 0
                var totalValue = 0
                var results = []
                for (timestamp in currentCategory[subcategory]["values"]) {
                    if (closestTimestamp < timestamp) {
                        closestTimestamp = timestamp
                    }
                    totalValue += currentCategory[subcategory]["values"][timestamp]
                    results.push({ "date": new Date(timestamp * 1000), "value": currentCategory[subcategory]["values"][timestamp]})
                }
                var currentID = "erinaStat-" + category + "-" + subcategory
                if (["cacheFilesCount", "responsePolarity"].includes(subcategory)) {
                    document.getElementById(currentID + "-Value").innerText = convert(currentCategory[subcategory]["values"][closestTimestamp])
                } else {
                    document.getElementById(currentID + "-Value").innerText = convert(totalValue)
                }
                createChart(currentID + "-Chart", results, am4core.color("#7ae2ff"))
            } else w(
                newError("An error occured on the server while retrieving " + String(subcategory))
            )
        } catch {
            newError("Error while adding subcategory: " + String(subcategory))
        }
    }

    fetch("/erina/api/admin/stats?token=" + window.localStorage.getItem("erinaAdminToken"))
    .then(function(data) {
        return data.json()
    })
    .then(function(data) {
        if (data.success == true) {
            data = data.data
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
                    newError("Error while adding category: " + String(category))
                }
            }
        } else {
            newError("An error occured while retrieving the stats")
        }
    })
}