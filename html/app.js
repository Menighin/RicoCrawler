function renderChart(chartId, dataKey, period) {
    
    let data = DATA;

    dataKey.split('.').forEach(function(k) {
        data = data[k];
    });
    
    let chart = {
        title: {
            text: 'OIOIOI'
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
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
        }
    };

    let series = [];
    for (let i = 0; i < data.length; i++) {
        
        let d = data[i];

        let daysToPlot = null;
        if (period === 'weekly') daysToPlot = 7;
        else if (period === 'biweekly') daysToPlot = 15;

        if (period !== 'monthly') {
            CONFIG.PROPS.forEach((p) => {
                if (d.hasOwnProperty(p.key)) {
                    let actualData = []; 
                    for (let j = d[p.key].length - 1, k = 0; j >= 0 && k < daysToPlot; j--, k++) {
                        actualData.push([ new Date(d.date[j]).getTime(), parseFloat(d[p.key][j]) ]);
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        } else { // Get one date by month
            let month = new Date(d.date[d.date.length - 1]).getMonth() + 1;

            CONFIG.PROPS.forEach((p) => {
                if (d.hasOwnProperty(p.key)) {

                    let actualData = []; 

                    for (let j = d[p.key].length - 1; j >= 0; j--) {

                        let currentDate = new Date(d.date[j]);
                        if (currentDate.getMonth() < month) {
                            actualData.push([ currentDate.getTime(), parseFloat(d[p.key][j]) ]);
                            month = currentDate.getMonth();
                        }
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        }
    }

    chart.series = series;

    Highcharts.chart(chartId, chart);
}


$(document).ready(() => {
    let template = $('#chart-template').html();

    let chartModel = {
        chartId: 'summary',
        dataKey: 'home.summary'
    };

    let rendered = Mustache.render(template, chartModel);

    $('#content').html(rendered)

});