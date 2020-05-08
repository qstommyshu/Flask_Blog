import os

class Config:
    SECRET_KEY='8404614bbac7423bb777ea1aba1f94c08d8ffd200c8975d4a5749f4b2072fe4b'
    #The database will be create in current dictory (///)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get('JUNK_EMAIL')
    MAIL_PASSWORD=os.environ.get('JUNK_EMAIL_PASSWORD')
    #Set to development model
    ENV = 'development'
    DEBUG = True
    TESTING = True
