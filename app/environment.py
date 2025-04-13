import os

from dotenv import load_dotenv
load_dotenv()

ENV = {
    'host': os.getenv('ITA_HOST', '0.0.0.0'),
    'debug': os.getenv('ITA_DEBUG', 'false').lower() == 'true',
    'port': os.getenv('ITA_PORT', 6789),
}

if(ENV['host'] == 'localhost'):
  ENV['host'] = '127.0.0.1'

print(ENV)
