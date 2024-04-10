from flask import Blueprint,render_template, redirect, url_for, request, flash
from .ModifMembres import ajouter_membre,get_profil
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .models import Membres

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        remember = True if request.form.get('remember') else False
        print(remember)
        if not login:
            flash('Le login doit être donné')
            return render_template("login.html")
        elif not mdp: 
            flash('Le mdp doit être donné')
            return render_template("login.html")
        else: 
            profil = get_profil(login)
            user = Membres.query.filter_by(login=login).first()
            if not check_password_hash(profil['password'], mdp):
                flash("L'identifiant ou le mot de passe ne sont pas bons")
            else:
                login_user(user,remember=remember)
                return render_template('aff_prof.html', profil=profil)
    return render_template("login.html")
            



@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        mail = request.form['mail']
        if not login:
            flash('Le login est nécéssaire')  
        elif not mdp: 
            flash('Le mot de passe est nécessaire')
        elif not mail: 
            flash('Le mail doit être fourni')
        else:
            try:
                ajouter_membre(login,mdp,mail)
                return redirect(url_for('main.index'))
            except: 
                flash("Le pseudonyme ou l'adresse mail saisie est déjà utilisé")

        return render_template('aj_membres.html')

    return render_template('aj_membres.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))