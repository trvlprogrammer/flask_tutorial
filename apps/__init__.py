from flask import Flask


def create_app():
    app = Flask(__name__)

    from apps.todo import bp as todo_bp
    app.register_blueprint(todo_bp)

    return app