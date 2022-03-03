class Config:
        SECRET_KEY = 'ZnZ^o#V9yuSF'

class DevelopmentConfig():
    DEBUG = True
    ORACLE_HOST = "localhost:1521/orcl"
    ORACLE_USER = "jsarmenteros"
    ORACLE_PASS = "123456"
    ORACLE_DB =""


config = {
    'development': DevelopmentConfig
}
