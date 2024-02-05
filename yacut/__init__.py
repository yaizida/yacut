import string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from settings import Config

# Constatns
CHARACTERS = string.ascii_letters + string.digits
BASE_URL = 'http://localhost/'
MAX_LENGTH = 16
CHEK_PATTERN = r'^[A-Za-z0-9]{,' + str(MAX_LENGTH) + r'}$'

#Application & DB
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from . import views, api_views, error_handlers
