from . import db
from flask_login import UserMixin

class Membres(UserMixin,db.Model):
    id_membre = db.Column(db.Integer, primary_key=True, unique=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(1000), unique=True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    mail = db.Column(db.String(100), unique=True, nullable = False)
    numero_tel = db.Column(db.String(100),unique=True, nullable = False)
    is_admin = db.Column(db.Boolean, unique = False, default =  False, nullable = False)
    is_confirmed = db.Column(db.Boolean, nullable = False, default = False)
    registered_on = db.Column(db.DateTime, nullable = False)
    confirmed_on = db.Column(db.DateTime, nullable = True)
    def get_id(self):
        return(self.id_membre)


