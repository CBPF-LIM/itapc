document.addEventListener('DOMContentLoaded', (event) => {
  // 1. intercept form id send post
  // 2. get cols field
  // 3. create a json from cols as {cols: processed_cols}
  // 4. processed cols is col string split by comma
  // 5. send post with json data

  var post_button = document.getElementById('post-button');
  var post_output = document.getElementById('post-output');
  var cols = document.getElementById('cols');

  var cmd_button = document.getElementById('cmd-button');
  var cmd_output = document.getElementById('cmd-output');
  var cmd = document.getElementById('cmd');

  var config_button = document.getElementById('config-button');
  var config_output = document.getElementById('config-output');
  var config = document.getElementById('config');

  function data_success(target, data) {
    target.innerHTML = data;
    target.classList.remove('error');
    target.classList.add('success');

    target.classList.remove('animate');
    void target.offsetWidth; // trigger reflow
    target.classList.add('animate');
  }

  function data_error(target, data) {
    target.innerHTML = data;
    target.classList.remove('success');
    target.classList.add('error');

    target.classList.remove('animate');
    void target.offsetWidth; // trigger reflow
    target.classList.add('animate');
  }

  post_button.addEventListener('click', function(event) {
    var processed_cols = cols.value.split(',');
    var json_data = {cols: processed_cols};
    fetch('/ita/exec', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(json_data),
    }).then(function(response) {
      return response.json();
    }).then(function(data) {
      data.response == 'success' ? data_success(post_output, "Ok") : data_error(post_output, data.message);
    }).catch(function(error) {
      alert('Error: ' + error);
    })
  })

  cmd_button.addEventListener('click', function(event) {
    fetch('/ita/exec?cmd=' + cmd.value)
    .then(response => {
      if(!response.ok) throw new Error('Network response was not ok');
      return response.text();
    })
    .then(data => {
      data_success(cmd_output, data);
    })
    .catch(error => {
      data_error(cmd_output, error);
    })
  })

  config_button.addEventListener('click', function(event) {
    fetch('/ita/exec?config=' + config.value)
    .then(response => {
      if(!response.ok) throw new Error('Network response was not ok');
      return response.text();
    })
    .then(data => {
      data_success(config_output, data);
    })
    .catch(error => {
      data_error(config_output, error);
    })
  })
})
