(function ($) {
    $.fn.extend( {
        tagPopularityChart: function() {
            var $chart = $(this);
            var $data = $chart.find('.chart-data');
            var $dataItems = $data.find('.chart-data-item');
            var labels = [];
            var data = [];

            $dataItems.each(function() {
                labels.push($(this).data('tag'));
                data.push($(this).data('count'));
            });

            var chart = new Chart(document.getElementById("chart_tag_popularity"), {
                type: 'bar',
                data: {
                  labels: labels,
                  datasets: [
                    {
                      label: "Count",
                      backgroundColor: $chart.find('.chart-fillColor').css('color'),
                      borderColor	: $chart.find('.chart-strokeColor').css('color'),
                      borderWidth: 2,
                      responsive: true,
                      data: data
                    }
                  ]
                },
                options: {
                  legend: { display: false },
                  title: { display: false },
                  scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1,
                        }
                    }]
                  }
                }
            });

            var updateChartColors = function(chart) {
                for (var i = 0; i < chart.datasets.length; ++i) {
                    chart.datasets[i]['fillColor'] = $chart.find('.chart-fillColor').css('color');
                    chart.datasets[i]['strokeColor'] = $chart.find('.chart-strokeColor').css('color');
                }

                chart.update();
            };

            $(document).on('theme:changed', function() {
                updateChartColors(chart);
            });
        }
    });



})(jet.jQuery);