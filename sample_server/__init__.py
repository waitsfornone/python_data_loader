from flask import Flask
from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()
DEBUG = True


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asdlfkja;lsdkfja;sldkfj'
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/tenders/Documents/code/python_data_loader/data/instructions.db'
    DB.init_app(app)

    return app
