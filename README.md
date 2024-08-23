# Ita PC

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

## App Configuration

To change the output and config files, create a file `app.ini` and optionally include:

```
output: table.csv
config: settings.ini
```
