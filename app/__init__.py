from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app(config_name):
    """this gone to return an app"""
    app = Flask(__name__)
    app.config.from_object(config[config_name] or config['default'])
    db.init_app(app)
    bootstrap.init_app(app)

    from .fiction import fiction
    app.register_blueprint(fiction)

    return app

