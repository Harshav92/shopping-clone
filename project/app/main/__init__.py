from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from ..config import app_config
from .routes.userroute import user
from .routes.categoryroute import category
from .routes.productroute import product

def create_app(environ):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_object(app_config[environ])
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(category, url_prefix="/category")
    app.register_blueprint(product, url_prefix="/product")


    return app