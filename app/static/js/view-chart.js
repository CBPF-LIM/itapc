document.addEventListener('DOMContentLoaded', (event) => {
  var generate_chart = document.getElementById('generate-chart');
  var x_axis = document.getElementById('x-axis');
  var y_axis = document.getElementById('y-axis');
  var x_name;
  var y_name;
  var experiment_id = document.getElementById('experiment-id').dataset.id;
  var update_channel = `update-${experiment_id}`
  var syncCheckbox = document.getElementById('sync-checkbox')

  var chartInstance = null;

  var socket = io.connect('http://' + document.location.hostname + ':' + location.port);
  var status = document.getElementById('connection-status');
  var status_message = document.getElementById('status-message');
  var first_connection = true;
  var chart_started = false;

  var loading = document.getElementById('loading-icon');
  var max_index;
  var rows = {}
  var header = []
  var x_values = []
  var y_values = []
  var new_points = []

  syncCheckbox.addEventListener('change', function() {
    setSync()
  })

  function get_axis_names() {
    x_name = x_axis.value;
    y_name = y_axis.value;
  }

  function create_chart() {
    chart_started = true;
    const ctx = document.getElementById('view-chart');

    var row = get_xy();

    removes = x_values.length - 100
    if (removes > 0) {
      x_values.shift(removes);
      y_values.shift(removes);
    }

    x_values.push(...row[0]);
    y_values.push(...row[1]);

    const data = {
      labels: x_values,
      datasets: [
        {
          label: y_name + " vs " + x_name,
          data: y_values,
          pointStyle: 'circle',
          pointRadius: 2,
          pointHoverRadius: 5
        }
      ]
    };

    if (chartInstance) {
      chartInstance.data = data
      chartInstance.update({
        duration: 0,
        lazy: false,
      });
    } else {
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
          responsive: true,
          animation: false,
          scales: {
            y: {
              beginAtZero: false
            }
          }
        }
      });
    }
  }

  async function button_click() {
    x_values = []
    y_values = []
    max_index = undefined
    await get_axis_names();
    await get_data();
    setSync()
  }

  function parse_rows() {
    var x = [];
    var y = [];

    for (var i = 0; i < Object.keys(rows).length; i++) {
      var row = rows[i];
      var cols = row['cols'];
      var id = row['id'];

      x.push(cols[x_index]);
      y.push(cols[y_index]);
    }

    return [x, y];
  }


  // function fetch_data(x_col, y_col) {
  //   fetch('/ita/view/chart/data', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify({x: x_col, y: y_col})
  //   }).then(response => response.json())
  //     .then(data => {
  //       create_chart(data.x, data.y);
  //     })
  //     .catch((error) => {
  //       console.error('Error:', error);
  //     });
  // }

  function stop_spinner() {
    setTimeout(function() {
      loading.classList.add('done');
    }, 500);

    setTimeout(function() {
      loading.classList.remove('spin');
    }, 3000);
  }

  function start_spinner() {
    loading.classList.remove('done');
    loading.classList.add('spin');
  }

  async function get_data() {
    var fetch_index = (max_index || 0) + 1;
    var url = `/ita/view/api/experiments/${experiment_id}/refresh/${fetch_index}`
    await fetch(url)
      .then(function(response) {
        stop_spinner();
        return response.json();
      })
      .then(function(data) {
        if(data.response == 'success') {
          header = data.header;
          max_index = parseInt(data.cols[data.cols.length - 1]['id']);
          new_points = data.cols;
          setTimeout(create_chart, 50);
        }
      })
      .catch(function(error) {
        stop_spinner();
      });
  }

function get_xy() {
    data = new_points
    var x_index = header.indexOf(x_name);
    var y_index = header.indexOf(y_name);

    var x = []
    var y = []

    for (var i = 0; i < data.length; i++) {
      var row = data[i];
      var cols = row['cols'];
      var id = row['id'];

      x.push(cols[x_index]);
      y.push(cols[y_index]);
    }
    new_points = []

    return [x, y];
  }

  function setSync() {
    if(syncCheckbox.checked) {
      socket.on(update_channel, function() {
        start_spinner();
        get_data();
        stop_spinner();
      });
    } else {
      socket.off(update_channel);
    }
  }

  generate_chart.addEventListener('click', button_click);

  socket.on('connect', function() {
      start_spinner();
      status.classList.add('on');
      status_message.classList.add('on');

      if (chart_started) {
        first_connection ? get_data() : reload();
      }

      first_connection = false;
  });

  socket.on('disconnect', function() {
      status.classList.remove('on');
      status_message.classList.remove('on');
      console.log('Disconnected');
  });
});
