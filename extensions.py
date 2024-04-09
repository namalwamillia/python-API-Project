from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from  flask_jwt_extended import JWTManager




# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flask_authors_db'

db = SQLAlchemy()  # Initialize SQLAlchemy after creating the app instance
migrate = Migrate() # Initialize Flask-Migrate with the app and db instances
bcrypt = Bcrypt()  # Initialize Flask-Bcrypt with the app instance
jwt = JWTManager() 



