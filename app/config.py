class Config:
    DEBUG = False
    TESTING = False
    DATABASE = 'ita_development.db'

class ConfigDevelopment(Config):
    DEBUG = True

class ConfigTest(Config):
    TESTING = True
    DATABASE = 'ita_test.db'

class ConfigProduction(Config):
    DATABASE = 'ita_production.db'
