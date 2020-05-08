from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_app.config import Config




db = SQLAlchemy()
bcrypt=Bcrypt()
Login_manager=LoginManager()
Login_manager.login_view='users.login'
Login_manager.login_message_category='info'

mail = Mail()

# app.config['SECRET_KEY']='8404614bbac7423bb777ea1aba1f94c08d8ffd200c8975d4a5749f4b2072fe4b'
# #The database will be create in current dictory (///)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# app.config['MAIL_SERVER']='smtp.googlemail.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USERNAME']=os.environ.get('JUNK_EMAIL')
# app.config['MAIL_PASSWORD']=os.environ.get('JUNK_EMAIL_PASSWORD')

# #Set to development model
# app.config['ENV'] = 'development'
# app.config['DEBUG'] = True
# app.config['TESTING'] = True





def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from flask_app.users.routes import users
    from flask_app.posts.routes import posts
    from flask_app.main.routes import main

    db.init_app(app)
    bcrypt.init_app(app)
    Login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app