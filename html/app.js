function getDataSeries(data, period) {
    let series = [];
    for (let i = 0; i < data.length; i++) {
        
        let d = data[i];

        let pointsToPlot = null;
        if (period === 'weekly' || period === 'biweekly' || period === 'monthly') pointsToPlot = 12;
        else if (period === 'daily') pointsToPlot = 14;

        if (period === 'daily') {
            CONFIG.PROPS.forEach((p) => {
                if (d.hasOwnProperty(p.key)) {
                    let actualData = []; 
                    for (let j = d[p.key].length - 1, k = 0; j >= 0 && k < pointsToPlot; j--, k++) {
                        actualData.push([ new Date(d.date[j]).getTime(), parseFloat(d[p.key][j]) ]);
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        } else if (period == 'monthly') { // Get one date by month
           
            CONFIG.PROPS.forEach((p) => {

                let date = new Date(d.date[d.date.length - 1])
                let month = date.getFullYear() + date.getMonth() + 1;

                if (d.hasOwnProperty(p.key)) {

                    let actualData = []; 

                    for (let j = d[p.key].length - 1, k = 0; j >= 0 && k < pointsToPlot; j--, k++) {

                        let currentDate = new Date(d.date[j]);
                        if (currentDate.getFullYear() + currentDate.getMonth() < month) {
                            actualData.push([ currentDate.getTime(), parseFloat(d[p.key][j]) ]);
                            month = currentDate.getMonth();
                        }
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        } else if (period === 'weekly' || period === 'biweekly') { // Get one date by week

            let spanDays = 7;
            if (period === 'biweekly') spanDays = 15;

            CONFIG.PROPS.forEach((p) => {

                let currentDate = new Date(d.date[d.date.length - 1])

                if (d.hasOwnProperty(p.key)) {

                    let actualData = []; 

                    for (let j = d[p.key].length - 1, k = 0; j >= 0 && k < pointsToPlot; j--, k++) {

                        let dateToCompare = new Date(d.date[j]);

                        let diffDays = Math.ceil(Math.abs(currentDate.getTime() - dateToCompare.getTime()) / (1000 * 60 * 60 * 24));

                        if (k == 0 || diffDays >= spanDays) {
                            actualData.push([ dateToCompare.getTime(), parseFloat(d[p.key][j]) ]);
                            currentDate = dateToCompare;
                        }
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        }
    }

    return series;
}

function getPercentageSeries(data, period) {
    let series = [];
    for (let i = 0; i < data.length; i++) {
        
        let d = data[i];

        let pointsToPlot = null;
        if (period === 'weekly' || period === 'biweekly' || period === 'monthly') pointsToPlot = 12;
        else if (period === 'daily') pointsToPlot = 14;

        if (period === 'daily') {
            CONFIG.PROPS.forEach((p) => {
                if (d.hasOwnProperty(p.key)) {
                    let actualData = []; 
                    for (let j = d[p.key].length - 1, k = 0; j > 0 && k < pointsToPlot; j--, k++) {

                        let todayValue = parseFloat(d[p.key][j]);
                        let yesterdayValue = parseFloat(d[p.key][j - 1]);
                        let diff = todayValue - yesterdayValue;
                        let percentValue = diff * 100 / yesterdayValue;

                        actualData.push([ new Date(d.date[j]).getTime(), percentValue]);
                    }
                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        } else if (period == 'monthly') { // Get one date by month
           
            CONFIG.PROPS.forEach((p) => {

                let date = new Date(d.date[d.date.length - 1])
                let month = date.getFullYear() + date.getMonth() + 1;

                if (d.hasOwnProperty(p.key)) {

                    let monthlyData = []; 

                    for (let j = d[p.key].length - 1, k = 0; j > 0 && k < pointsToPlot; j--, k++) {

                        let currentDate = new Date(d.date[j]);
                        if (currentDate.getFullYear() + currentDate.getMonth() < month) {

                            monthlyData.push([ currentDate.getTime(), parseFloat(d[p.key][j]) ]);
                            month = currentDate.getMonth();
                        }
                    }

                    let actualData = [];
                    for (let j = monthlyData.length; j > 0; j--) {
                        let thisMonth = monthlyData[j];
                        let lastMonth = monthlyData[j-1];
                        let diff = thisMonth - lastMonth;
                        let percentValue = diff * 100 / lastMonth;
                        actualData.push(percentValue);
                    }

                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        } else if (period === 'weekly' || period === 'biweekly') { // Get one date by week

            let spanDays = 7;
            if (period === 'biweekly') spanDays = 15;

            CONFIG.PROPS.forEach((p) => {

                let currentDate = new Date(d.date[d.date.length - 1])

                if (d.hasOwnProperty(p.key)) {

                    let weeklyData = []; 

                    for (let j = d[p.key].length - 1, k = 0; j >= 0 && k < pointsToPlot; j--, k++) {

                        let dateToCompare = new Date(d.date[j]);

                        let diffDays = Math.ceil(Math.abs(currentDate.getTime() - dateToCompare.getTime()) / (1000 * 60 * 60 * 24));

                        if (k == 0 || diffDays >= spanDays) {
                            weeklyData.push([ dateToCompare.getTime(), parseFloat(d[p.key][j]) ]);
                            currentDate = dateToCompare;
                        }
                    }

                    let actualData = [];
                    for (let j = weeklyData.length; j > 0; j--) {
                        let thisWeek = weeklyData[j];
                        let lastWeek = weeklyData[j-1];
                        let diff = thisWeek - lastWeek;
                        let percentValue = diff * 100 / lastWeek;
                        actualData.push(percentValue);
                    }

                    series.push({name: d.name + ' ' + p.label, data: actualData});
                }
            });
        }
    }

    return series;
}

function renderChart(btn, chartId, dataKey, period) {
    
    // Disable buttons to enable the clicked one
    if (btn != null) {
        $('#' + chartId + '-container .chart-filter .btn').each(function() {
            $(this).removeClass('active');
        });

        $(btn).addClass('active');
    }

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

    chart.series = getPercentageSeries(data, period);

    Highcharts.chart(chartId, chart);
}

function loadPage(li, key) {

    // Setting the active styled button page
    if (li != null) {
        $('#menu-list li').each(function() {
            $(this).removeClass('active');
        });
        $(li).addClass('active');
    }


    let template = $('#chart-template').html();
    
    let chartModels = CONFIG.PAGES[key];

    $('#content').html('');

    chartModels.forEach((model) => {
        let rendered = Mustache.render(template, model);
        $('#content').append(rendered)
        $('#content').append('<hr />')
        renderChart(null, model.chartId, model.dataKey, 'daily');
    });
}

function hideAllSeries(chartId) {
    $.each($('#' + chartId).highcharts().series, function(i, series) {
        series.setVisible(false, false);
    });

}

$(document).ready(() => {

    loadPage(null, 'home');

});