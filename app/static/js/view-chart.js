document.addEventListener('DOMContentLoaded', (event) => {
  var generate_chart = document.getElementById('generate-chart');
  var x_axis = document.getElementById('x-axis');
  var y_axis = document.getElementById('y-axis');
  var chartInstance = null;


  function create_chart(x, y) {
    const ctx = document.getElementById('view-chart');

    const data = {
      labels: x,
      datasets: [
        {
          label: y_axis.value + " vs " + x_axis.value,
          data: y,
          pointStyle: 'circle',
          pointRadius: 10,
          pointHoverRadius: 15
        }
      ]
    };

    if (chartInstance) {
      chartInstance.data.labels = x;
      chartInstance.data.datasets[0].data = y;
      chartInstance.update();
    } else {
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      });
    }

  }

  function button_click() {
    x_col = x_axis.value;
    y_col = y_axis.value;
    console.log(x_col, y_col);
    if (x_col != "" && y_col != "") {
      fetch_data(x_col, y_col);
    } else {
      alert("Please select columns for X-axis and Y-axis");
    }
  }

  function fetch_data(x_col, y_col) {
    fetch('/ita/view/chart/data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({x: x_col, y: y_col})
    }).then(response => response.json())
      .then(data => {
        create_chart(data.x, data.y);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  generate_chart.addEventListener('click', button_click);
});
