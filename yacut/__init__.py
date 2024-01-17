from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Config

BASE_URL = 'http://localhost/'
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from . import views, api_views, error_handlers
