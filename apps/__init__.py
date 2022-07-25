from flask import Flask
from config import Config #import class Config from config.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy() #define orm
migrate = Migrate() #define migration
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
login.login_message_category = "danger"

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(Config) #read and apply config from Config class 
    
    db.init_app(app) #initiate db
    migrate.init_app(app,db) #initiate migration
    login.init_app(app)

    from apps.todo import bp as todo_bp
    app.register_blueprint(todo_bp)

    from apps.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

from apps import models #import all class in models.py