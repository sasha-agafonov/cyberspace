from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch = True)
admin = Admin(app,template_mode='bootstrap3')
logging.basicConfig(filename = 'logs', filemode='w', format='%(levelname)s:%(message)s')

from app import views, models
