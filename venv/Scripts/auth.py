from flask import Blueprint,render_template, redirect, url_for, request, flash
from .ModifMembres import ajouter_membre

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        mail = request.form['mail']
        if not login:
            flash('login est nécéssaire')        
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
    return 'Logout'