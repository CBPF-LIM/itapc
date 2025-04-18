/* TODO:
 *    - Settings still comes from a file config.ini
 *    - move config and to database
 *    - "cmd" and "config" route must be change in api (processGet in ita/__init__.py)
 *    - update route api routes
 *
 */

function clean_output(text) {
  return text
    .split('\n')
    .map(line => line.trim())
    .join('\n');
}

function loadSimpleTemplate() {
  const template = `
    "cols": [1, 2, 3],
    "exp": "{{experiment.id}}",
    "device": "ita-tools",
    "t0": "1",
    "t1": "2"`.trim();
  document.getElementById('cols').value = clean_output(template);
}

function loadAuthTemplate() {
  const template = `
    "cols": [1, 2, 3],
    "exp": "{{experiment.id}}",
    "device": "ita-tools",
    "t0": "1",
    "t1": "2",
    "apikey": "your_api_key_here"`.trim()

  document.getElementById('cols').value = clean_output(template);
}

document.addEventListener('DOMContentLoaded', (event) => {
  var post_button = document.getElementById('post-button');
  var post_output = document.getElementById('post-output');
  var cols = document.getElementById('cols');

  var cmd_button = document.getElementById('cmd-button');
  var cmd_output = document.getElementById('cmd-output');
  var cmd = document.getElementById('cmd');

  var config_button = document.getElementById('config-button');
  var config_output = document.getElementById('config-output');
  var config = document.getElementById('config');

  var experiment_id = document.getElementById('experiment-id').dataset.id;

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
    var json_data

    try {
      json_data = JSON.parse('{' + cols.value + "}");
    } catch (e) {
      data_error(post_output, "Invalid JSON. Check syntax!");
      return;
    }

    fetch('/api', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(json_data),
    }).then(function(response) {
      return response.json();
    }).then(function(data) {
      data.response == 'success' ? data_success(post_output, "Ok") : data_error(post_output, data.message);
    }).catch(function(data) {
      alert('Error: ' + data);
    })
  })

  cmd_button.addEventListener('click', function(event) {
    fetch(`/api?exp=${experiment_id}&cmd=${cmd.value}`)
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
    fetch(`/api?exp=${experiment_id}&config=${config.value}`)
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

  loadSimpleTemplate();
})
