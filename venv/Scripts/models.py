from . import db
from flask_login import UserMixin

class Membres(UserMixin,db.Model):
    id_membre = db.Column(db.Integer, primary_key=True, unique=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))
    mail = db.Column(db.String(100), unique=True)
    def get_id(self):
        return(self.id_membre)


