class config:
    secret_key = 'YmO{!z`i/m<b-[+'

class DevelopmentConfig(config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'rusttab'
    SECRET_KEY = 'YmO{!z`i/m<b-['
    

config = {
    'development': DevelopmentConfig,
}