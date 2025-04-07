document.addEventListener('DOMContentLoaded', (event) => {
  var socket = io.connect('http://' + document.location.hostname + ':' + location.port);
  var status = document.getElementById('connection-status');
  var status_message = document.getElementById('status-message');
  var first_connection = true;
  var loading = document.getElementById('loading-icon');
  var max_index = 0;
  var experiment_id = document.getElementById('experiment-id').dataset.id;
  var update_channel = `update-${experiment_id}`
  var followCheckbox = document.getElementById('follow-checkbox');
  var syncCheckbox = document.getElementById('sync-checkbox')

  followCheckbox.addEventListener('change', function() {
    table = document.getElementById('output-table')

    if (this.checked) {
      window.scrollTo(0, document.body.scrollHeight);
      this.parentElement.classList.remove('order-0')
      this.parentElement.classList.add('order-1')
      table.classList.remove('order-1')
      table.classList.add('order-0')
    } else {
      this.parentElement.classList.remove('order-1')
      this.parentElement.classList.add('order-0')
      table.classList.remove('order-0')
      table.classList.add('order-1')
    }
  })

  syncCheckbox.addEventListener('change', function() {
    setSync()
  })

  function updateTable(data) {
    var table = document.getElementById('output');

    var rows = data.cols;
    var header = data.header;

    if(rows.length) {
      var data_info = document.getElementById('data-info');
      data_info.classList.add('has');
    }

    if(max_index == 0 && header) {
      var tr = document.createElement('tr');

      var th = document.createElement('th');
      th.innerHTML = "ID";
      tr.appendChild(th);

      for(var i = 0; i < header.length; i++) {
        var item = String(header[i]);
        var th = document.createElement('th');
        th.innerHTML = item;
        tr.appendChild(th);
      }
      table.appendChild(tr);
    }

    for(var i = 0; i < rows.length; i++) {
      var id = rows[i]['id']
      var cols = rows[i]['cols']

      var tr = document.createElement('tr');

      var td = document.createElement('td');
      td.innerHTML = id;
      tr.appendChild(td);

      for(var j = 0; j < cols.length; j++) {
        var item = String(cols[j])
        var td = document.createElement('td');
        td.innerHTML = item;
        tr.appendChild(td);
      }
      table.appendChild(tr);
    }

    max_index = rows[rows.length - 1]['id'];


    rows = output.querySelectorAll('tr')
    removes = rows.length - 101
    if(removes > 0) {
      for (var i = 0; i < removes ; i++) {
        output.removeChild(rows[i+1]);
      }
    }


    var followCheckbox = document.getElementById('follow-checkbox');
    if (followCheckbox && followCheckbox.checked && (window.scrollY + window.innerHeight + 50 >= document.body.offsetHeight)) {
      document.documentElement.style.setProperty('scroll-behavior', 'auto', 'important');
      document.body.style.setProperty('scroll-behavior', 'auto', 'important');
      window.scrollTo(0, document.body.scrollHeight);
    }
  }

  function reload() {
    setTimeout(function() {
      console.log('Server reconnected');
      get_data();
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
    var experiment_id = document.getElementById('experiment-id').dataset.id;
    var fetch_index = max_index ? max_index + 1: 0;
    var url = `/ita/view/api/experiments/${experiment_id}/refresh/${fetch_index}`
    fetch(url)
      .then(function(response) {
        stop_spinner();
        return response.json();
      })
      .then(function(data) {
        if(data.response == 'success') {
          updateTable(data);
        }
      })
      .catch(function(error) {
        stop_spinner();
      });
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

  setSync()
});
