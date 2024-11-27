class Config:
    SECRET_KEY ='IHOhd(//&&%(/)ljhgsjhd128973848UHUHhhsgwgnkpipai'
    DEBUG      = True

class ConfigDevelopment(Config):
    MYSQL_HOST     = 'localhost'
    MYSQL_USER     = 'root'
    MYSQL_PASSWORD = 'mysql'
    MYSQL_DB       = 'justeat'
    
    '''
    #Pythonawhere
    MYSQL_HOST      ='justeat.mysql.pythonawhere.services.com'
    MYSQL_USER      ='justeat'
    MYSQL_PASSWORD  ='alfaro890$
    MYSQL_DB        ='justete$justeat'
    '''
    

class MailConfig(Config):
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USE_SSL  = False
    MAIL_USERNAME ='alan.avila1645@alumnos.udg,mx'
    MAIL_PASSWORD = 'neqs jqbw nike elnj'
    MAIL_DEFAULT_SENDER ='alan.avila1645.@alumnos.mx'
    MAIL_ASCII_ATACHMENTS = True


Config = {
    'development': ConfigDevelopment,
    'mail'       : MailConfig

} 


    