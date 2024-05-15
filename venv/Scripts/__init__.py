from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_mail import Mail, Message
from .extensions import mail



db=SQLAlchemy()
# init SQLAlchemy so we can use it later in our models

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/baoch/ST/venv/Scripts/BDD_velos.db'
app.config['SECURITY_PASSWORD_SALT'] = "very-important"

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = "Vous devez être connecté pour accéder à cette page"
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

from .booking import booking as booking_blueprint
app.register_blueprint(booking_blueprint)

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

    
app.config['MAIL_DEFAULT_SENDER'] = "noreply@flask.com"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = False
app.config['MAIL_USERNAME'] = "baochautran1247@gmail.com"
app.config['MAIL_PASSWORD'] = "sptw yovx dbjn igra"

mail.init_app(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
