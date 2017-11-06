from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import logging.config


DB = SQLAlchemy()
DEBUG = True


def create_app():
    app = Flask(__name__)
    # logging.config.fileConfig('logging.ini')    
    # myLogger = logging.getLogger('flaskApp')
    # app.logger_name = myLogger
    app.config['SECRET_KEY'] = 'asdlfkja;lsdkfja;sldkfj'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tenders/Documents/code/python_data_loader/data/instructions.db'
    DB.init_app(app)

    return app
