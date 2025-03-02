// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

// Area Chart Example
$(document).ready(function () {
  $.ajax({
    url: "/registros_saidas",
    type: "GET",
    success: function (data) {
      var ctx = document.getElementById("myAreaChart").getContext("2d");
      var myLineChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: data.dias_semana,
          datasets: [
            {
              label: "Saídas",
              lineTension: 0.3,
              backgroundColor: "rgba(2,117,216,0.2)",
              borderColor: "rgba(2,117,216,1)",
              pointRadius: 5,
              pointBackgroundColor: "rgba(2,117,216,1)",
              pointBorderColor: "rgba(255,255,255,0.8)",
              pointHoverRadius: 5,
              pointHoverBackgroundColor: "rgba(2,117,216,1)",
              pointHitRadius: 50,
              pointBorderWidth: 2,
              data: data.Saidas,
            },
          ],
        },
        options: {
          scales: {
            xAxes: [
              {
                time: {
                  unit: "date",
                },
                gridLines: {
                  display: false,
                },
                ticks: {
                  maxTicksLimit: 7,
                },
              },
            ],
            yAxes: [
              {
                ticks: {
                  min: 0,
                  max: data.media,
                  maxTicksLimit: 5,
                },
                gridLines: {
                  color: "rgba(0, 0, 0, .125)",
                },
              },
            ],
          },
          legend: {
            display: false,
          },
        },
      });
    },
  });
});
