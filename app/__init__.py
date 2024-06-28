from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
mail = Mail()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from app import routes, models

        @app.before_request
        def create_admin():
            if not hasattr(app, 'admin_created'):
                if not User.query.filter_by(username='admin').first():
                    admin = User(username='admin', email='admin@example.com', is_admin=True)
                    admin.set_password('adminpassword')
                    db.session.add(admin)
                    db.session.commit()
                app.admin_created = True

    return app