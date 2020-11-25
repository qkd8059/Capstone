/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        '2020',
        '2021',
        '2022',
        '2023',
        '2024',
        '2025',
        '2026'
      ],
      datasets: [{
        data: [
          2000,
          2134,
          2089,
          2234,
          2295,
          2256,
          2331
        ],
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
var ctxD = document.getElementById("doughnutChart").getContext('2d');
var myLineChart = new Chart(ctxD, {
type: 'doughnut',
data: {
labels: ["AAPL", "MSFT", "AMZN", "FB", "JPM", "BAC", "WMT", "V"],
datasets: [{
data: [38, 17, 6, 8, 15, 5, 4, 7],
backgroundColor: ["#dc3545", "#fd7e14", "#ffc107", "#007bff", "#28a745", "#17a2b8", "#6f42c1", "#6c757d"],
hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
}]
},
options: {
responsive: true
}
});
