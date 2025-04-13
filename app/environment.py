import os

ENV = {
    'host': os.getenv('ITA_HOST', '0.0.0.0'),
    'debug': os.getenv('ITA_DEBUG', 'false').lower() == 'true',
    'port': os.getenv('ITA_PORT', 6789),
    'app_secret': os.getenv('ITA_SECRET', 'default-secret-key')
}
