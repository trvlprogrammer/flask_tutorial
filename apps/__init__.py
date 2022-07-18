from flask import Flask
from config import Config #import class Config from config.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy() #define orm
migrate = Migrate() #define migration

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(Config) #read and apply config from Config class 
    
    db.init_app(app) #initiate db
    migrate.init_app(app,db) #initiate migration

    from apps.todo import bp as todo_bp
    app.register_blueprint(todo_bp)

    return app

from apps import models #import all class in models.py