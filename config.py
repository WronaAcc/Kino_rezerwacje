import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YOURSECRETKEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:YOURPASSWORD@localhost/kino_rezerwacje'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'YOURMAILSERVER'
    MAIL_PORT = YOURMAILPORT
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOURMAILUSERNAME'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'YOURMAILPASSWORD'
    ADMINS = ['YOURADMIN']
    WTF_CSRF_ENABLED = True
