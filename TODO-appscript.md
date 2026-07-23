New ItaServerless

# POST

## Append data

endpoint: /api&route=data

payload:

{
  "cols": array of any type,
  "exp": experiment_id,
  "device": "device hash",
  "t0": "millis just before measure",
  "t1": "millis just after measure",
  "apikey": "APIkey configured in Experiment->Settings->Config"
}

returns:

{
  "response": "success"
}

## Find or Create Experiment

endpoint: /api&route=exp

payload:

{
  "header": JSON array
  "name": Expetiment name
}

returns:

{
  "response": "success",
  "id": "experiment id",
  "new": "True of False"
}

## Find or Create Device

endpoint: /api&route=device

payload:

{
  "name": Device human name
  "hash": unique code for device
}

returns:

{
  "response": "success",
  "id": "device id",
  "new": "True of False"
}

# GET

Note: Must remove all GET routes because AppScript receive send headers, so apikey will be sent open

## Get single Config

http://localhost:6789/api/exp/<experiment id>/config/<config key>

## Run cmd

http://localhost:6789/api/exp/<experiment id>/cmd/<cmd>


# Novo Ita Appscript


Como incorporar os novos componentes do novo ItaServer?

* Experiment
* Device
* Data
* Authentication


## Option 1: Full compatible

* Init
  * Create tab "Experiments"
  * Create tab "Devices"
* FindOrCreateExperiment
  * Create (if not exists) a new tab "Experiment-<id>"
  * Create (if not exists) a new tab "Config-<id>"
  * Search columns ID in Experiments
    * Set? Get extra columns
    * Unset? Add now row with ID = max+1 in Experiments tab
* FindOrCreateDevice
  * Search columns ID in Experiments
    * Set? Get extra columns
    * Unset? Add now row with ID = max+1 in Device tab
* AddData
  * add row with data
* Authentication
  * Easy check Config


## Option 2: Lite Compatible

[.] Init
  [.] Create tab "Experiments"
  [.] Create tab "Devices"
  [.] Create tab "Config"
[.] FindOrCreateExperiment
  [.] Save experiment name in Experiments tab
[.] FindOrCreateDevice
  [.] Save device name in Devices tab
[.] AddData
  [.] Create a "data-<experiment id>" tab, if not existe
  [.] Add row in "data-<experiment id>"
[.] Authentication
  [.] Easy check Config

Change backend response

from: {"response": "success/error", ...}
to {"status": "ok/error", ...}
