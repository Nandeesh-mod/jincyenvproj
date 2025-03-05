from flask import Flask, render_template
from config import Config
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def make_app():
    app = Flask(__name__,template_folder='templates',static_folder="static",static_url_path="/")

    config = Config()
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)

    from routes import add_routes

    add_routes(app, db)

    return app

def getdb():
    db = SQLAlchemy(make_app)
    return db



