// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

$(document).ready(function () {
  $.ajax({
    url: "/saidasFuncionario",
    type: "GET",
    success: function (data) {
      var ctx = document.getElementById("ChartFuncionario");
      var myLineChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [{
            label: "Revenue",
            backgroundColor: "rgba(2,117,216,1)",
            borderColor: "rgba(2,117,216,1)",
            data: data.values,
          }],
        },
        options: {
          scales: {
            xAxes: [{
              time: {
                unit: 'day'
              },
              gridLines: {
                display: false
              },
              ticks: {
                maxTicksLimit: 6
              }
            }],
            yAxes: [{
              ticks: {
                min: 0,
                max: data.media,
                maxTicksLimit: 5
              },
              gridLines: {
                display: true
              }
            }],
          },
          legend: {
            display: false
          },
          tooltips: {
            callbacks: {
              label: (tooltipItem, data) => {
                return formatMoney(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]);
              },
            },
          },
        }
      });
    }
  });
});


function formatMoney(n, c, d, t) {
  c = isNaN(c = Math.abs(c)) ? 2 : c, d = d == undefined ? "," : d, t = t == undefined ? "." : t, s = n < 0 ? "-" : "", i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "", j = (j = i.length) > 3 ? j % 3 : 0;
  return s + (j ? i.substr(0, j) + t : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
}