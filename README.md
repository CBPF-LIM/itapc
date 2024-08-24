# Ita PC

Bored About Ita AppScript?

Usage:

* Create a directory to work
* Just type `itapc`!

Now ItaPC server is up and running without needing any configuration!

Want configuration?

* Just type `itapc sample`!

Now you have `app_sample.ini` and `config_sample.ini` files. Rename them (remove the `_sample`) and edit.

## Table of Contents

- [Ita PC](#ita-pc)
  - [Table of Contents](#table-of-contents)
  - [Install](#install)
  - [The "config tab"](#the-config-tab)
  - [The "data tab"](#the-data-tab)
    - [CSV format](#csv-format)
  - [App Ini](#app-ini)
    - [Host](#host)
    - [Port](#port)
    - [Output:](#output)
    - [Output Mode:](#output-mode)
    - [Config file](#config-file)
    - [Debug](#debug)
  - [Config Ini](#config-ini)
    - [Coll names](#coll-names)
  - [API](#api)
    - [Base URL](#base-url)
    - [GET Endpoints](#get-endpoints)
    - [POST endpoint](#post-endpoint)
  - [Options for testing the POST method](#options-for-testing-the-post-method)
    - [curl:](#curl)
    - [wget:](#wget)
    - [httpie:](#httpie)
    - [Windows Powershell:](#windows-powershell)
    - [GUI options:](#gui-options)
    - [Python:](#python)

## Install

Using pip:

```sh
$ pip3 install git+https://github.com/CBPF-LIM/itapc.git
```

> Note: If "pip3" is not found, try nust "pip"

After install, run itapc lika a normal terminal cmd:

```sh
$ itapc
```

The run folder will be used for data.csv and config.ini

## The "config tab"

Use a config.ini file:

```csv
enabled: 1
interval: 1000
col1: x
col2: y
col3: z
col_index: Counter
col_ms: Millis
col_timestamp: Moment
```

## The "data tab"

Output will be in data.csv

### CSV format

- With header
- separator: TAB
- number without quotes, others quoted

## App Ini

Default:

```json
  host: 0.0.0.0         # External access by default
  port: 6789
  output: data.csv
  output_mode: append
  config: config.ini
  debug: False
```

Create a new file `app.ini` or create a sample running `itapc sample`.

File is just many `key: value` lines.

**Options:**

### Host

Controls the server access. Options: ip, host or a 'alias':

* aliases for 127.0.0.1: localhost, local, private or intenal:
* aliases for 0.0.0.0: public, external, all or any:

### Port

Integer. Values below 1024 require root access

### Output:

Filename of your data's output. If it doesn't exist, it will be created.

### Output Mode:

How to handle the output file?

* append: reuse the file
* timestamp: create a new file every time with timestamp. Format: YYYYMMDDHHMMSS
    * Example: data.csv_20240101120000.csv
* fresh: clear the data file at start (**danger!**)

### Config file

File to configure the data and data behavior.

### Debug

Ita is based on Flask. This controls the Flask debug mode. Many human options:

String aliases for:

* True:
    * 1, yes, y, t, on, enable, enabled, ok
* False: aliases for False:
    * 0, no, n, f, off, disable, disabled, ko

## Config Ini

Controls the data. Can be used to interact with the server.

File is just many `key: value` lines.

### Coll names

col_index: Change "Index" col name.
col_ms: Change "ms" col name.
col_timestamp: Change "Timestamp" col name

col1, col2, col3, ...: Change the col names of the data. "col1" is the "first data received", no counting the three above.

## API

This is how you interact with ItaPC.

### Base URL

If you already use ItaAppscript, just change your "base URL" from:

`https://script.google.com/macros/s/<Google Appscript Token>/exec"`

to

`http://<ip or name>:<port>/ita/exec`

e.g: For

* host: 0.0.0.0
* port: 6789
* and supose your machine IP isIP is 192.168.0.100

the base endpoint will be:

`http://192.168.0.100:6789/ita/exec`

### GET Endpoints

**Commands:**

All configs:

`http://IP:PORT/ita/exec?cmd=configs`

Send all configs at config.ini.

Specific config:

`http://IP:PORT/ita/exec?config=key`

Send just the config <key>.

Last index on CSV:

`http://IP:PORT/ita/exec?cmd=last-index`

Seek the CSV file and returns the last index.

### POST endpoint

You can send POST JSON data to base URL (http://IP:PORT/ita/exec). The JSON content:

```
{
  "cols": [index, e1, e2, ..., en]
}
```

* index is the "data id" and you must manually control and increment.
    * ItaPC compares the new index with last index and refuses do write a line when equal.
* e1, e2, ..., en: array with any tipe of data to be included in CSV as a line.

ItaPC will insert this line:

1: TimeStamp with format: YYYYMMDDHHMMSS
2: Index. The first param of `cols`
3: Milliseconds since first data arrived. It starts at zero.
4 and beyond: all the `e1, e2, ..., en` data, each in a col.

**Notes:**

1. If CSV do not exist, it will be created with a HEADER. Look at the "config.ini" to create custom columns names.
2. The ESP32 Ita Firmware ask on boot what is the last index and resume the index at that value plus one (next index)

## Options for testing the POST method

If you want to test POST, here are some options

### curl:

```sh
  curl -X POST -H "Content-Type: application/json" -d'{"cols":[1,2,3]}' "http://192.168.0.100:6789/ita/exec"
```

* -X POST: use POST
* -H: Add an HTTP HEADER, to say "we are sendind a json"
* -d: the string representation of the JSON
* Last param: just the URL. To evade problems, use quoted.

### wget:

```sh
wget --header="Content-Type: application/json" --post-data='{"cols":[1,2,3]}' --output-document=- "http://192.168.0.100:6789/ita/exec"
```

* --header: Add an HTTP HEADER, to say "we are sendind a json"
* --post-data: string representation of JSON. If used, POST will be selected as send methotd
* --output-document: You can select a file t o save the output. Using dash "-" means "use the terminal"
* last param: just the URL. To evade problems, use quoted.

### httpie:

Very simple to use:

```sh
$ http POST http://192.168.0.100:6789/ita/exec cols:=[1,2,3]
```

### Windows Powershell:

```sh
Invoke-RestMethod -Uri "http://192.168.0.100:6789/ita/exec" -Method POST -Body '{"cols":[1,2,3]}' -ContentType "application/json"
```

### GUI options:

* Insomnia (https://insomnia.rest/download)
* Postman (https://www.postman.com/downloads/)

### Python:

A simple script with some customization? Here is a minimal funcional script using package `requests`:

If not installed:

```
$ pip install requests
```

```python
import requests

url = "http://192.168.0.100:6789/ita/exec"
data = {"cols": [1, 2, 3]}

requests.post(url, json=data).text
```
