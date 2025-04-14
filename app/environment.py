import os

from dotenv import load_dotenv
load_dotenv()

ENV = {
    'environment': os.getenv('ITA_ENVIRONMENT', 'development'),
    'host': os.getenv('ITA_HOST', '0.0.0.0'),
    'debug': os.getenv('ITA_DEBUG', 'false').lower() == 'true',
    'port': os.getenv('ITA_PORT', 6789),
}

if(ENV['host'] == 'localhost'):
    ENV['host'] = '127.0.0.1'

def config_class():
    if ENV['environment'] == 'development':
        from app.config import ConfigDevelopment as Config
    elif ENV['environment'] == 'testing':
        from app.config import ConfigTest as Config
    elif ENV['environment'] == 'production':
        from app.config import ConfigProduction as Config
    else:
        raise ValueError(f"Unknown environment: {ENV['environment']}")
        exit(0)

    return Config
