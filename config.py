import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:Void240901!@localhost/kino_rezerwacje'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'poczta.o2.pl'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'Karlosss123@o2.pl'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'RGKNZTBUHUC2HWC5'
    ADMINS = ['Karlosss123@o2.pl']
    WTF_CSRF_ENABLED = True
True