import secret, os

class Config:
    MYSQL_HOST = secret.dbHost
    MYSQL_USER = secret.dbUser
    MYSQL_PASSWORD = secret.dbPassword
    MYSQL_DB = secret.dbName
    
    MAIL_SERVER = secret.smtpDomain
    MAIL_PORT = secret.smtpPort
    MAIL_USERNAME = secret.smtpUser
    MAIL_PASSWORD = secret.smtpPw
    MAIL_DEFAULT_SENDER = secret.smtpUser
    MAIL_USE_TLS = True

    TESTING = True #EMails didnt send if true

    SECRET_KEY = os.urandom(16)