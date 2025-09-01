import os
from db_config import db_username, db_password, db_hostname, db_database

class STATIC_CONFIG:
    SECRET_KEY = os.urandom(256)
    MYSQL_USER = db_username
    MYSQL_PASSWORD = db_password
    MYSQL_DB = db_database
    MYSQL_HOST = db_hostname
    MYSQL_CURSORCLASS = "DictCursor"
