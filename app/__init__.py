from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


my_app = Flask(__name__)
my_app.config.from_object(Config)

db = SQLAlchemy(my_app)
migrate = Migrate(my_app, db)

from app import views, models

