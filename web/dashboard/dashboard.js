/* globals Chart:false, feather:false */

function generateLineChart(lineData) {
  // Graphs
  var ctx = document.getElementById('myChart')
  ctx.innerHTML = '';
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: lineData['dates'],
      datasets: [{
        label: 'Your Portfolio',
        data: lineData['ret'],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 1,
        pointBackgroundColor: '#007bff'
      },
      {
        label: '60/40 Portfolio',
        data: lineData['ret_6040'],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#EA3711',
        borderWidth: 1,
        pointBackgroundColor: '#EA3711'
      },
      {
        label: 'SPY',
        data: lineData['ret_spy'],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#2FEA11',
        borderWidth: 1,
        pointBackgroundColor: '#2FEA11'
      }
      ]
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
        display: true,
        position: 'right',
        labels: { usePointStyle: true }
      }
    }
  })
}


function generatePieChart(pieData) {
  /*f (this.readyState == 4 && this.status == 200) {
    myObj = JSON.parse(this.responseText);
    for (x in myObj) {
      tickers.push(myObj[x].ticker);
      weights.push(myObj[x].weight);
    }
  }*/
  document.getElementById("doughnutChart").innerHTML = '';
  var ctxD = document.getElementById("doughnutChart").getContext('2d');
  var myLineChart = new Chart(ctxD, {
    type: 'doughnut',
    data: {
      labels: pieData['tickers'],
      datasets: [{
        data: pieData['weights'],
        backgroundColor: ["#dc3545", "#fd7e14", "#ffc107", "#007bff", "#28a745", "#17a2b8", "#6f42c1", "#6c757d"],
        hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
      }]
    },
    options: {
      responsive: true
    }
  });
}

function generateAssetAllocationTable(assetData) {
  var txt = "<table class='table table-striped table-sm'><thead><tr><th>Asset</th><th>Value</th><th>Weight</th></tr></thead><tbody>"
  for (var x = 0; x < assetData["tickers"].length; x++) {
    txt += "<tr><td>" + assetData['tickers'][x] + "</td>";
    txt += "<td>" + assetData['prices'][x] + "</td>";
    txt += "<td>" + assetData['weights'][x] + "%</td></tr>";
  }
  txt += "</tbody></table>"
  document.getElementById("weights-table").innerHTML = txt;
}

function generateStatisticalMeasurementTable(statData) {
  var txt = "<table class='table table-striped table-sm'><thead><tr><th>Measure</th><th>Value</th></tr></thead><tbody>"

  txt += "<tr><td>" + 'Returns' + "</td>";
  txt += "<td>" + statData['rets'] + "</td></tr>";
  txt += "<tr><td>" + 'Standard Deviation' + "</td>";
  txt += "<td>" + statData['std'] + "</td></tr>";
  txt += "<tr><td>" + 'Sharpe Ratio' + "</td>";
  txt += "<td>" + statData['sharpe'] + "</td></tr>";
  txt += "</tbody></table>";
  document.getElementById("stats-table").innerHTML = txt;
}

function generateportfoliomenu(Names) {
  let paperclip = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-paperclip"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"></path></svg>';
  var txt = "";
  for (var x = 0; x < Names['names'].length; x++) {
    var current = "";
    if (Names['names'][x] == Names['current']) {
      current = " active";
    }
    y = x + 1;
    txt += '<li class="nav-item"><a class="nav-link' + current + '" onclick="generatePortfolio(' + x + ')">'+ paperclip + 'Portfolio ' + y + '</a></li>'
  }
  document.getElementById("portmenu").innerHTML = txt;
}

var responseJSON;

function generatePortfolio(portfolio_number) {
  var xhr = new XMLHttpRequest();
  xhr.onload = function () {
    if (xhr.status == 200) {
      responseJSON = JSON.parse(xhr.responseText);

      generateLineChart(responseJSON[0]);
      generatePieChart(responseJSON[1])

      generateAssetAllocationTable(responseJSON[2]);
      generateStatisticalMeasurementTable(responseJSON[3]);

      generateportfoliomenu(responseJSON[4]);
    } else {

      alert('Portfolios not ready yet!');
    }
  }
  var match = document.cookie.match(/session_id=[^;]+/);
  if (match === null) {
    window.location.href = '/sign-in/sign-in.html';
    return;
  }
  var payload = JSON.stringify({
    portfolio: portfolio_number,
    session_id: match[0].substr(11)
  });
  xhr.open("POST", "/backend/dashboard-line-chart");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(payload);
}

(function () {
  'use strict'
  feather.replace()

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/backend/check-session-id');
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = () => {
    console.log(xhr);
    if (xhr.status != 200 || xhr.responseText == "logged out")
      window.location.href = '/sign-in/sign-in.html';
    else
      generatePortfolio(0);
  };
  var payload = JSON.stringify({
    cookie: document.cookie
  });
  xhr.send(payload);

})()
