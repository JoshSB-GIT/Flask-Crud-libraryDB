class Configuration:
    SECRET_KEY = '3d6f!#45a5@*fc124+45'

class DevelopmentConfig(Configuration):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_DB = 'librarydb'
    
    
config = {
    'development': DevelopmentConfig
}