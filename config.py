class Config:
    SECRET_KEY ='IHOhd(//&&%(/)ljhgsjhd128973848UHUHhhsgwgnkpipai'
    DEBUG      = True

class ConfigDevelopment(Config):
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB       = 'justeat'

config = {
    'development': ConfigDevelopment
}