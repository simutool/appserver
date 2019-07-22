var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
    type: 'bubble',
    data: {
        labels: "Kennzeichnung",
        datasets: [
            {
                label: ["Element 1"],
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255,221,50,1)",
                data: [{x:10, y:9, r:20}]
            }, {
                label: ["Element 2"],
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255,221,50,1)",
                data: [{x:10, y:5, r:40}]
            }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
