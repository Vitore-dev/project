from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__,template_folder='templates')
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'hackdb.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app , db)

    ##from .routes import register_routes
    ##register_routes(app,db)
    ##from . import routes
    ##routes.init_app(app)
    from .authroutes import init_app
    init_app(app)


    return app