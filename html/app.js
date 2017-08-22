function buildChart(title) {
    return {
        title: {
            text: title
        },
        yAxis: {
            title: {
                text: 'R$'
            }
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                month: '%e. %b',
                year: '%b'
            },
            title: {
                text: 'Date'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        }
    }
}

function buildDailyChart(data, title) {
    let chart = buildChart(title);

    let series = [];
    for (let i = 0; i < data.length; i++) {
        
        let d = data[i];

        if (d.hasOwnProperty('actual')) {
            let actualData = []; 
            for (let j = 0; j < d.actual.length; j++) {
                actualData.push([ new Date(d.dates[j]).getTime(), d.actual[j] ])
            }
            series.push({name: d.name + ' (Actual)', data: actualData})
        }

        if (d.hasOwnProperty('applied')) {
            let appliedData = []; 
            for (let j = 0; j < d.applied.length; j++) {
                appliedData.push([ new Date(d.dates[j]).getTime(), d.applied[j] ])
            }
            series.push({name: d.name + ' (Applied)', data: appliedData})
        }
    }

    chart.series = series;

    Highcharts.chart('chart', chart);
}

Highcharts.chart('summary-daily', {
        title: {
            text: 'Solar Employment Growth by Sector, 2010-2016'
        },
    
        yAxis: {
            title: {
                text: 'Number of Employees'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
    
        series: [{
            name: 'Installation',
            data: [43934, 52503, 57177, 69658, 97031, 119931, 10000, 154175]
        }, {
            name: 'Manufacturing',
            data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
        }, {
            name: 'Sales & Distribution',
            data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
        }, {
            name: 'Project Development',
            data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
        }, {
            name: 'Other',
            data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
        }]
    
    });