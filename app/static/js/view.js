document.addEventListener('DOMContentLoaded', (event) => {
  var socket = io.connect('http://' + document.location.hostname + ':' + location.port);
  var status = document.getElementById('connection-status');
  var status_message = document.getElementById('status-message');
  var first_connection = true;
  var loading = document.getElementById('loading-icon');
  var max_index = 0;

  function appendOutput(data) {
    var table = document.getElementById('output');

    var rows = data;

    if(rows.length) {
      var data_info = document.getElementById('data-info');
      data_info.classList.add('has');
    }

    for(var i = 0; i < rows.length; i++) {
      var cols = rows[i];
      var tr = document.createElement('tr');
      for(var j = 0; j < cols.length; j++) {
        var item = String(cols[j])
        if(j == 1) max_index = parseInt(item)
        item = item.replace(/^"(.*)"$/, '$1');
        var td = document.createElement('td');
        td.innerHTML = item;
        tr.appendChild(td);
      }
      table.appendChild(tr);
    }

  }

  function reload() {
    setTimeout(function() {
      alert('Server reconnected. Refreshing page to get new data.');
      location.reload();
    }, 100);
  }

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

  function get_data() {
    var fetch_index = max_index ? max_index + 1: 0;
    //fetch('http://' + document.location.hostname + ':' + location.port + '/ita/view/lines/from_index/' + (fetch_index))
    fetch('/ita/view/lines/from_index/' + (fetch_index))
      .then(function(response) {
        stop_spinner();
        return response.json();
      })
      .then(function(data) {
        if(data.response == 'success') {
          appendOutput(data.data);
        }
      })
      .catch(function(error) {
        stop_spinner();
      });
  }

  socket.on('connect', function() {
      start_spinner();
      status.classList.add('on');
      status_message.classList.add('on');

      first_connection ? get_data() : reload();
      first_connection = false;
  });

  socket.on('disconnect', function() {
      status.classList.remove('on');
      status_message.classList.remove('on');
      console.log('Disconnected');
  });

  socket.on('done', function() {
    start_spinner();
    get_data();
    stop_spinner();
  });
});
