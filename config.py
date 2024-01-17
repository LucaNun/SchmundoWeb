import secret, os

class Config:
    MYSQL_HOST = secret.dbHost
    MYSQL_USER = secret.dbUser
    MYSQL_PASSWORD = secret.dbPassword
    MYSQL_DB = secret.dbName
    SECRET_KEY = os.urandom(16)