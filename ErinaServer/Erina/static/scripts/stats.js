function PageInitialize() {
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
    var chartElements = document.getElementsByTagName("erinastat-list-item-chart");
    for (var i = 0; i < chartElements.length; i++) {
        try {
            createChart(chartElements.item(i).id, templateData, am4core.color("#7ae2ff"))
            //chartElements.item(i).parentElement.parentElement.appendChild(chartElements.item(i))
        } catch {
            console.log("Error")
        }   
    }
}