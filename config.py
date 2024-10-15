import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'YOURSECRETKEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://root:YOUR_ROOT_PASSWORD@localhost/kino_rezerwacje'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration
    MAIL_SERVER = 'YOUR_MAIL_SERVER'
    MAIL_PORT = 'YOUR_MAIL_PORT'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'YOUR_MAIL_USERNAME'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'YOUR_MAIL_PASSWORD'
    ADMINS = ['YOUR_ADMINS']
    WTF_CSRF_ENABLED = True