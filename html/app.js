function renderChart(chartId, dataKey, period) {
    
    let data = DATA;

    dataKey.split('.').forEach(function(k) {
        data = data[k];
    });
    
    let chart = {
        title: {
            text: $('#' + chartId + '-title').val()
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
            let date = new Date(d.date[d.date.length - 1])
            let month = date.getFullYear() + date.getMonth() + 1;

            CONFIG.PROPS.forEach((p) => {
                if (d.hasOwnProperty(p.key)) {

                    let actualData = []; 

                    for (let j = d[p.key].length - 1; j >= 0; j--) {

                        let currentDate = new Date(d.date[j]);
                        if (currentDate.getFullYear() + currentDate.getMonth() < month) {
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

function loadPage(li, key) {
    let template = $('#chart-template').html();
    
    let chartModels = CONFIG.PAGES[key];

    $('#content').html('');

    chartModels.forEach((model) => {
        let rendered = Mustache.render(template, model);
        $('#content').append(rendered)
        $('#content').append('<hr />')
        renderChart(model.chartId, model.dataKey, 'weekly');
    });
}

$(document).ready(() => {

    loadPage(null, 'home');

});