from flask import Flask
from config import Config #import class Config from config.py

def create_app(config_class=Config): 
    app = Flask(__name__)
    app.config.from_object(Config) #dread and apply config from Config class 

    from apps.todo import bp as todo_bp
    app.register_blueprint(todo_bp)

    return app