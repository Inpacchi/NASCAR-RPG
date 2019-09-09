from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config

from models import webapp

webapp = Flask(__name__)
webapp.config.from_object(Config)
db = SQLAlchemy(webapp)
migrate = Migrate(webapp, db)
login = LoginManager(webapp)

from app import routes
