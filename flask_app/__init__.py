from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY']='8404614bbac7423bb777ea1aba1f94c08d8ffd200c8975d4a5749f4b2072fe4b'


#The database will be create in current dictory (///)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
Login_manager=LoginManager(app)
Login_manager.login_view='login'
Login_manager.login_message_category='info'


#Set to development model
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

from flask_app import routes