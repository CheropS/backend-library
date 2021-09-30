import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import app_config

app = Flask('__name__')

CORS(app)
jwt = JWTManager(app)
app.config.from_object(app_config['production'])
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
