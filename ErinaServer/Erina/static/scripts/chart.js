// Add Loading Animation
am4core.useTheme(am4themes_animated);

// Improving Performance
am4core.options.queue = true;
am4core.options.onlyShowOnViewport = true;

// Functions that create various sparklines
function createChart(id, data, color) {
    // Create chart instance
    var container = am4core.create(id, am4core.Container);
    container.layout = "grid";
    container.fixedWidthGrid = false;
    container.width = am4core.percent(100);
    container.height = am4core.percent(100);

    var chart = container.createChild(am4charts.XYChart);
    chart.width = am4core.percent(100);
    chart.height = am4core.percent(100);

    chart.data = data;

    //chart.padding(20, 5, 2, 5);

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.labels.template.disabled = true;
    dateAxis.startLocation = 0.5;
    dateAxis.endLocation = 0.7;
    dateAxis.cursorTooltipEnabled = true;
    dateAxis.groupData = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.min = 0;
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.renderer.baseGrid.disabled = true;
    valueAxis.renderer.labels.template.disabled = true;
    valueAxis.cursorTooltipEnabled = false;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.lineY.disabled = true;
    chart.cursor.behavior = "none";

    var series = chart.series.push(new am4charts.LineSeries());
    //series.tooltipText = "{date}: [bold]{value}";
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "value";
    series.tensionX = 0.8;
    series.strokeWidth = 2;
    series.stroke = color;

    series.fillOpacity = 0.8;

    var fillModifier = new am4core.LinearGradientModifier();
    fillModifier.opacities = [0.3, 0];
    fillModifier.offsets = [0, 1];
    fillModifier.gradient.rotation = 90;
    series.segments.template.fillModifier = fillModifier;


    document.querySelector("#" + id + " > div > svg > g > g:nth-child(2) > g:nth-child(2) > g > g:nth-child(3)").style.display = "none"
    chartsRegistry.push(chart)
    return chart;
}

function updateChart(chart, newData, reloadAnimation=false){
  //Setting the new data to the graph
  chart.dataProvider = newData;

  //Updating the graph to show the new data
  chart.validateData();
  
  if (reloadAnimation == true) {
    chart.animateAgain();
  }
}

/****
createChart("erinaChart", [
    { "date": new Date(2018, 0, 1, 8, 0, 0), "value": 57 },
    { "date": new Date(2018, 0, 1, 9, 0, 0), "value": 27 },
    { "date": new Date(2018, 0, 1, 10, 0, 0), "value": 24 },
    { "date": new Date(2018, 0, 1, 11, 0, 0), "value": 59 },
    { "date": new Date(2018, 0, 1, 12, 0, 0), "value": 33 },
    { "date": new Date(2018, 0, 1, 13, 0, 0), "value": 46 },
    { "date": new Date(2018, 0, 1, 14, 0, 0), "value": 20 },
    { "date": new Date(2018, 0, 1, 15, 0, 0), "value": 42 },
    { "date": new Date(2018, 0, 1, 16, 0, 0), "value": 59, "opacity": .9}
], am4core.color("#7ae2ff"))
*/