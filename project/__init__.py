import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User}

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from project.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


def create_database(app):
    with app.app_context():
        db.create_all()
    print('Created Database!')
