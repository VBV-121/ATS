# Flask library are imported here
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#Define app name
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

#Set up keys for database
app.config['SECRET_KEY']='1a858e5d5f93ac4338efe291b34f9d8c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#create object of database
db = SQLAlchemy(app)

#Create a encryption object
bcrypt = Bcrypt(app)

#Create login manager to keep track of users 
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#call home page
from frontend import routes