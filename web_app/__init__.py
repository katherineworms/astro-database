from flask import Flask
from flask_mysqldb import MySQL
from static_config import STATIC_CONFIG

# Citation for the useage of Flask-Mysqldb package:
# Date: 2023-11-12
# Based on:
# Source URL: https://pypi.org/project/Flask-MySQLdb/
mysql = MySQL()

def create_app(config_class = STATIC_CONFIG):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mysql.init_app(app)

    # Register main blueprint
    from web_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
