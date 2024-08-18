from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

flask = Flask(__name__)
flask.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todosdb.sqlite'
flask.config['SECRET_KEY'] = b'9doeiikdie9'

db = SQLAlchemy()
db.init_app(flask)

bcrypt = Bcrypt()
bcrypt.init_app(flask)


login_manager = LoginManager()
login_manager.init_app(flask)

from CTWApp import routes, models
