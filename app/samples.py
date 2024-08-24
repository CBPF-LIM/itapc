def app_ini():
    return """# Rename this file to app.ini
#
# Port
# Integer. Values below 1024 require root access
port: 6789

# Host
#   Options: ip, host or a 'alias':
#     aliases for 127.0.0.1: localhost, local, private or intenal:
#     aliases for 0.0.0.0: public, external, all or any:
host: localhost

# Debug
#   Controls Flask debug mode.
#   Many human options:
#     aliases for True: 1, yes, y, t, on, enable, enabled, ok
#     aliases for False: 0, no, n, f, off, disable, disabled, ko
debug: false

# Output file:
#   File to receive data. If it doesn't exist, it will be created.
output: data.csv

# Output Mode:
#   How to handle the output file?
#     append: reuse the file
#     timestamp: create a new file every time with timestamp. Format: YYYYMMDDHHMMSS
#         Example: data.csv_20240101120000.csv
#     fresh: clear file at start
output_mode: timestamp

# Config file
# File to configure the data and data behavior
config: config.ini
"""

def config_ini():
    return """Rename this file to config.ini
col1: x
col2: y
col3: z
col4: w
col_index: Index
col_ms: ms
col_timestamp: Timestamp
"""
