from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
# init SQLAlchemy so we can use it later in our models
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'hi'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/baoch/BV/venv/Scripts/BDD_velos.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Membres

    @login_manager.user_loader
    def load_user(member_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return Membres.query.get(int(member_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app