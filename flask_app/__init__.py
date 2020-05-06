import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY']='8404614bbac7423bb777ea1aba1f94c08d8ffd200c8975d4a5749f4b2072fe4b'


#The database will be create in current dictory (///)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
Login_manager=LoginManager(app)
Login_manager.login_view='login'
Login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='Tommyswift258@gmail.com'
app.config['MAIL_PASSWORD']='123456monkey'
mail = Mail(app)


#Set to development model
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

from flask_app import routes