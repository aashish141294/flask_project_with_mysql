from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import mysql.connector


UPLOAD_FOLDER = 'website/static/uploads/'
db = SQLAlchemy()
DB_NAME = "flask_project1"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/flask_project1'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    db.init_app(app)
 
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    
 
    from website.controller.views import views
    from website.controller.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users
    with app.app_context():
        db.create_all()
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        
