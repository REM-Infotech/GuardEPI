// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily =
  '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = "#292b2c";

$(document).ready(function () {
  $.ajax({
    url: "/registros_saidas",
    type: "GET",
    success: function (data) {
      var ctx = document.getElementById("myBarChart");
      var myLineChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.dias_semana,
          datasets: [
            {
              label: "Revenue",
              backgroundColor: "rgba(2,117,216,1)",
              borderColor: "rgba(2,117,216,1)",
              data: data.Saidas,
            },
          ],
        },
        options: {
          scales: {
            xAxes: [
              {
                time: {
                  unit: "day",
                },
                gridLines: {
                  display: false,
                },
                ticks: {
                  maxTicksLimit: 6,
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
                  display: true,
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
