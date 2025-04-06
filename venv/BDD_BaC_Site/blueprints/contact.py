from flask import Blueprint,render_template, redirect, url_for, request, flash
from ..functions.ModifMembres import ajouter_membre,get_profil,changer_mdp, confirm, changer_mdp_oublie
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from ..tools.models import Membres
from flask_session import Session
import datetime
from ..tools.decorators import logout_required
from ..ttoken import generate_token, confirm_token
from ..mmail import send_email
from ..functions.contact_functions import putMessage



contact = Blueprint('contact', __name__)

@contact.route('/contact_us', methods = ["GET", "POST"])
@login_required
def contact_us():
    if request.method == "POST":
        type = request.form["type"]
        titre = request.form['titre']
        message = request.form['message']
        putMessage(current_user.id_membre, message,titre, type)
        return redirect(url_for('contact.contact_us'))
    return render_template("Contact_Us.html", login=current_user.login, admin=current_user.is_admin)

