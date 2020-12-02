/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  var obj, dbParam, xmlhttp, myObj, x, txt = "";
  var dates, values = [];
  obj = { chart: "line", cookie: document.cookie };
  dbParam = JSON.stringify(obj);
  xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      myObj = JSON.parse(this.responseText);
      for (x in myObj) {
        datess.push(myObj[x].date);
        values.push(myObj[x].value);
      }
    }
  }
  xmlhttp.open("POST", "backend/dashboard-line-chart/", true);
  xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xmlhttp.send(dbParam);

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates,
      datasets: [{
        data: values,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
})()

//doughnut
var obj, dbParam, xmlhttp, myObj, x, txt = "";
var tickers, weights = [];
obj = { chart: "pie", cookie: document.cookie };
dbParam = JSON.stringify(obj);
xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    myObj = JSON.parse(this.responseText);
    for (x in myObj) {
      tickers.push(myObj[x].ticker);
      weights.push(myObj[x].weight);
    }
  }
}
xmlhttp.open("POST", "backend/dashboard-pie-chart/", true);
xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xmlhttp.send(dbParam);

var ctxD = document.getElementById("doughnutChart").getContext('2d');
var myLineChart = new Chart(ctxD, {
  type: 'doughnut',
  data: {
    labels: tickers,
    datasets: [{
      data: weights,
      backgroundColor: ["#dc3545", "#fd7e14", "#ffc107", "#007bff", "#28a745", "#17a2b8", "#6f42c1", "#6c757d"],
      hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
    }]
  },
  options: {
    responsive: true
  }
});
