TODO:
  tests:
    * Check old test and covnert to new pytest hierarch
    * PRIORITY: create API tests
  exp32:
    * test all types of endpoints
    * We can change t0 and t1 to dt and still send the millis
  ItaAppScript (now ItaServerless)
    * After all set in ItaServer, update the Library to match the new ItaServer
    * now the ItaServer needs exp and device in POST
    * we removed the index! it was very important to check if data got received. Now we have to to search another way
      to handle GAS limitations
    * in GAS, exp can be meny possibilities:
      * exp -> tab target, so the Sheet will be a multi-data sheet
      * exp -> just an extra column or an rejected data
    * device
      * before the removal of index, we thought about a [index, device] pair to validate repeated data.
        Now we have to ensure that with other means.
        The esp32 POST must got a valid "created" response so it can discard the measure and go on.
        SOLUTION: millis() as checksum! record the millis and compares with the last saved data for equality. Equal? data is repeted! responde with 200 and hopy now the ESP32 get the answer.
Done:
  experiments:
    * fix headers in edit
    * fix first generated header
    * chart:
      * check selects for columns
  AppSettings:
    * X ~CRUD or use the app.ini?~
    * Use simple .env files for server configuration
  tests:
    * pytest fixed. Added device model test and and example
  devices:
    * CRUD
  ApiKeys:
    * Create CRUD for apikeys
      * Name: Only for easy identification
      * hash: used as key
    * Use the post data to reject
    * Can disable apikeys system
    * Enabled in experiments's Setting's config
      * Authentication on: The config must have a key api_key_id
      * Authentication off: Remove the api_key_id from config
      * api_key_id points to a ApiKey id
      * The POST must include a key 'apikey' which value is equal with Apikey hash defined in config
