import os
from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from datetime import datetime
 
app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ROOT_DIR+'//database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy()
db.init_app(app)

bcrypt = Bcrypt()

migrate = Migrate()
ma = Marshmallow()
