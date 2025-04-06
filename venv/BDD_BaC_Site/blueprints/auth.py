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



auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
@logout_required
def login():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        remember = True if request.form.get('remember') else False
        if not login:
            flash('Le login doit être donné')
            return render_template("login.html")
        elif not mdp: 
            flash('Le mdp doit être donné')
            return render_template("login.html")
        else: 
            try:
                profil = get_profil(login)
                user = Membres.query.filter_by(login=login).first()
                if not check_password_hash(profil['password'], mdp):
                    flash("L'identifiant ou le mot de passe ne sont pas bons")
                else:
                    login_user(user,remember=remember)
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)
                    else:
                        return redirect(url_for('main.index'))
            except:
                flash("Votre données n'existent pas")
                return redirect(url_for('auth.login'))
    return render_template("Connexion.html")
            



@auth.route('/signup', methods=['GET', 'POST'])
@logout_required
def signup():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        omdp =  request.form['omdp']
        mail = request.form['mail']
        numero_tel = request.form['numero_tel']
        registered_on = datetime.datetime.now().strftime('%Y-%m-%d %X')
        if not login:
            flash('Le login est nécéssaire')  
        elif not mdp: 
            flash('Le mot de passe est nécessaire')
        elif not mail: 
            flash('Le mail doit être fourni')
        elif not numero_tel:
            flash('Le numéro de téléphone doit être fourni')  
        elif not omdp:
            flash('Veuillez réécrire votre mot de passe')
        elif omdp != mdp : 
            flash('Les mots de passe ne correspondent pas')    
        else:        
            ajouter_membre(login,mdp,mail,numero_tel,registered_on)
            user = Membres.query.filter_by(login=login).first()
            print(user)
            login_user(user)
            token =  generate_token(mail)
            confirm_url = url_for('auth.confirm_email',token=token, _external=True)
            html = render_template('confirm_mail.html', confirm_url=confirm_url)
            subject = "Confirmez votre mail"
            send_email(mail,subject,html)
            flash("Confirmez votre boîte pour confirmer votre identité")
            return redirect(url_for('main.index'))
            #except: 
                #flash("Le pseudonyme ou l'adresse mail ou le numéro de téléphone saisi est déjà utilisé")

        return render_template('Inscription.html')

    return render_template('Inscription.html')

@auth.route('/confirm/<token>')
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.")
        return redirect(url_for("main.profile"))
    mail = confirm_token(token)
    user = Membres.query.filter_by(mail=current_user.mail).first_or_404()
    if user.mail == mail:
        confirm(mail)
        flash("Vous avez confirmé votre adresse mail. Merci!")
    else:
        flash("Le lien de confirmation est invalide ou a expiré.")
    return redirect(url_for("main.index"))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    return render_template('unconfirmed.html')

@auth.route('/resend')
@login_required
def resend_confirmation():
    token = generate_token(current_user.mail)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    html = render_template('confirm_mail.html', confirm_url=confirm_url)
    subject = "Confirmez votre mail"
    send_email(current_user.mail, subject, html)
    flash("Un nouveau mail de confirmation vient d'être envoyé")
    return redirect(url_for('auth.unconfirmed'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/changepassword',methods=['GET','POST'])
@login_required
def changepassword():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        new_mdp = request.form['new_mdp']
        if not login: 
            flash('Le login est nécessaire')
        elif not mdp: 
            flash('Le mot de passe est nécessaire')
        elif not new_mdp:
            flash('Le nouveau mot de passe est nécessaire')
        else: 
            
            profil = get_profil(login)
            changer_mdp(profil['login'],mdp,new_mdp)
            
        return redirect(url_for('main.index'))
    return render_template('changepass.html')

           
@auth.route('/forgottenpassword',methods=['GET','POST'])
def forgottenpassword():
    if request.method == 'POST':
        mail = request.form['mail']
        if not login: 
            flash('Le login est nécessaire')
        try:
            user = Membres.query.filter_by(mail=mail).first_or_404()
        except:
            user = None
        if not user: 
            flash("Le profil n'existe pas")
            return redirect(url_for('auth.forgottenpassword'))
        else: 
            token = generate_token(user.mail)
            confirm_url = url_for('auth.forgottenpasswordconfirm', token=token, _external=True)
            html = render_template('confirm_password.html', confirm_url=confirm_url)
            subject = "Réinitialiser votre mot de passe"
            send_email(user.mail, subject, html)  
            flash("Consultez votre boîte mail pour continuer la procédure de changement de mot de passe") 
        return redirect(url_for('main.index'))
    return render_template('MdpOublieMail.html')


@auth.route('/forgottenpasswordconfirm/<token>',methods=['GET','POST'])
def forgottenpasswordconfirm(token):
    mail = confirm_token(token)
    try: 
        user = Membres.query.filter_by(mail=mail).first_or_404()
        if request.method == "POST":
            new_mdp = request.form['new_mdp']
            onew_mdp = request.form['onew_mdp']
            if new_mdp == onew_mdp: 
                changer_mdp_oublie(user.login,new_mdp)
                logout_user()
                flash("Mot de passe changé, veuillez vous reconnecter")
                return redirect(url_for('auth.login'))
            else: 
                flash("Les mots de passe ne correspondent pas")
                return redirect(url_for('auth.forgottenpassword'))
        return render_template('MdpOublie.html')
    except: 
        flash("Erreur, le mail n'existe pas")
        return redirect(url_for('main.index'))
    


    