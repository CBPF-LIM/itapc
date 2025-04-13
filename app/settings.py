import os

env = {
  'host': os.getenv('ITA_HOST', '0.0.0.0'),
  'debug': os.getenv('ITA_DEBUG', 'false').lower() == 'true',
  'port': os.getenv('ITA_PORT', 6789)
}
