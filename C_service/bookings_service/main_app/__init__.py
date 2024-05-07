from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

CORS(app=app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

from main_app import routes
from main_app import models
