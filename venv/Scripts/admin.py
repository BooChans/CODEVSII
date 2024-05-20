from flask import Blueprint,render_template, redirect, url_for, request, flash,session
from .ModifMembres import ajouter_membre,get_profil,changer_mdp, confirm, changer_mdp_oublie
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from .models import Membres
from flask_session import Session
import datetime
from .decorators import logout_required, admin_required
from .ttoken import generate_token, confirm_token
from .mmail import send_email
from .admin_functions import add_one_bike,bike_list,remove_bike,user_list,MakeAdmin,remove_user,get_users,get_admin_users,get_admins,history,search_history,delete_history,RemoveAdmin



admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=["GET", "POST"])
@login_required
@admin_required
def admin_tools():
    admin = current_user.is_admin
    user = current_user.login
    return render_template('GestionAdmin.html',user=user, admin=admin)

@admin.route('/admin_velos',methods=["GET","POST"])
@login_required
@admin_required
def admin_velos():
    velos = bike_list()
    if request.method == "POST":
        action = request.form['action'].split(" ")
        if action[0] == "change":
            None
        elif action[0] == "remove": 
            session['removed_bike'] = action[1]
            return render_template('VerificationSuppressionVelo.html',velo=action[1])
        elif action[0] == "confirm_removal":
            remove_bike(session['removed_bike'])
            return redirect(url_for('admin.admin_velos'))
        elif action == "abandon":
            return redirect(url_for('admin.admin_velos'))
    return render_template('AdminVelos.html',velos=velos, len_velos=len(velos))


@admin.route('/add_bike',methods=["GET","POST"])
@login_required
@admin_required
def add_bike():
    if request.method == "POST":
        print(request.form)
        hauteur = request.form['hauteur']
        longueur = request.form['longueur']
        statut = request.form['statut']
        if not hauteur or not longueur or not statut:
            flash("La taille et l'état sont nécéssaires")        
        else:
            print("hi")
            add_one_bike(hauteur,longueur,statut)
            return redirect(url_for('admin.admin_tools'))
    return render_template('AjouterVelo.html')


@admin.route('/admin_users',methods=["GET","POST"])
@login_required
@admin_required
def admin_users():
    users = user_list()
    if request.method == "POST":
        action = request.form['action'].split(" ")
        if action[0] == "search":
            session['admin'] = True if 'admin' in request.form else False
            if "login" in request.form:
                login = request.form['login']
                session['searched_logins'] = login
                return redirect(url_for('admin.admin_searchusers'))
            if "login" not in request.form: 
                session['login'] = None
                return redirect(url_for('admin.admin_searchusers'))
            if not login and not admin: 
                return redirect(url_for('admin.admin_users'))
        elif action [0] == "admin":
            session['login_to_be_admin'] = action[1]
            return redirect(url_for('admin.admin_admin_confirm'))
        elif action[0] == "remove":
            session['login_to_be_removed'] = action[1]
            return redirect(url_for('admin.admin_remove_user_confirm'))
        elif action[0] == "remove_admin":
            session['login_to_be_removed_admin'] = action[1]
            return redirect(url_for('admin.admin_remove_admin_confirm'))
    return render_template('ListeUtilisateurs.html', users=users, len_user=len(users))

@admin.route('/admin_searchusers',methods=["GET","POST"])
@login_required
@admin_required
def admin_searchusers():
    if session['admin']:
        if session['searched_logins']:
            users = get_admin_users(session['searched_logins'])
        else: 
            users = get_admins()
    else: 
        users = get_users(session['searched_logins'])
    if request.method == "POST":
        action = request.form['action'].split(" ")
        if action[0] == "search":
            session['admin'] = True if 'admin' in request.form else False
            if "login" in request.form:
                login = request.form['login']
                session['searched_logins'] = login
                return redirect(url_for('admin.admin_searchusers'))
            if "login" not in request.form: 
                session['login'] = None
                return redirect(url_for('admin.admin_searchusers'))
            if not login and not admin: 
                return redirect(url_for('admin.admin_users'))
        elif action [0] == "admin":
            session['login_to_be_admin'] = action[1]
            return redirect(url_for('admin.admin_admin_confirm'))
        elif action[0] == "remove":
            session['login_to_be_removed'] = action[1]
            return redirect(url_for('admin.admin_remove_user_confirm'))
        elif action[0] == "remove_admin":
            session['login_to_be_removed_admin'] = action[1]
            return redirect(url_for('admin.admin_remove_admin_confirm'))
    return render_template('ListeUtilisateurs.html', users=users, len_user=len(users))


@admin.route('/admin_history',methods=["GET","POST"])
@login_required
@admin_required                    
def admin_history():
    try: 
        historique,dh_historique = search_history(session['search_login'],session['search_id_velo'],session['search_date'])
    except:
        historique,dh_historique = history()
    if request.method == "POST":
        if request.form['action'] == 'delete_all':
            return redirect(url_for('admin.admin_delete_history'))
        if request.form['action'] == 'search':
            session['search_login'] = request.form['login']
            session['search_id_velo'] = request.form['id_velo']
            if request.form['date']:
                date_list=request.form['date'].split("T")
                session['search_date']=date_list[0]+" 00:00:00"
                print(session['search_date'])
            else: 
                session['search_date']=None
            return redirect(url_for('admin.admin_history'))
    return render_template('AdminHistorique.html', historique = historique, dh_historique=dh_historique, len_historique = len(historique))


@admin.route('/admin_search_history',methods=["GET","POST"])
@login_required
@admin_required                    
def admin_search_history():
    try:
        historique,dh_historique = search_history(session['search_login'],session['search_id_velo'],session['search_date'])
        if request.method == "POST":
            if request.form['action'] == 'delete_all':
                return redirect(url_for('admin.admin_delete_history'))
            if request.form['action'] == 'search':
                session['search_login'] = request.form['login']
                session['search_id_velo'] = request.form['id_velo']
                if request.form['date']:
                    date_list=request.form['date'].split("T")
                    session['search_date']=date_list[0]+" 00:00:00"
                    print(session['search_date'])
                else: 
                    session['search_date']=None
                return redirect(url_for('admin.admin_search_history'))
    except: 
        return redirect(url_for('admin.admin_history'))
    return render_template('AdminHistorique.html', historique = historique, dh_historique=dh_historique, len_historique = len(historique))

@admin.route('/admin_delete_history',methods=["GET","POST"])
@login_required
@admin_required  
def admin_delete_history():
    if request.method == "POST":
        action = request.form['action']
        if action == "delete_all":
            admin_delete_history()
            return redirect(url_for('admin.admin_tools'))
        if action == "abandon":
            return redirect(url_for('admin.admin_history'))
    return render_template('VerificationSuppressionHistorique.html')

@admin.route('/admin_admin_confirm', methods = ["GET", "POST"])
@login_required
@admin_required 
def admin_admin_confirm():
    try: 
        user = session['login_to_be_admin']
        if request.method == "POST":
            action = request.form['action']
            if action == "confirm":
                MakeAdmin(session['login_to_be_admin'])
                return redirect(url_for('admin.admin_users'))
            if action == "abandon":
                return redirect(url_for('admin.admin_users'))
    except: 
        return redirect(url_for('admin.admin_users'))
    return render_template('VerificationPassageAdmin.html')

@admin.route('/admin_remove_user_confirm', methods = ["GET", "POST"])
@login_required
@admin_required 
def admin_remove_user_confirm():
    try:
        user = session['login_to_be_removed']
        if request.method == "POST":
            action = request.form['action']
            if action == "confirm":
                remove_user(user)
                return redirect(url_for('admin.admin_users'))
            if action == "abandon":
                return redirect(url_for('admin.admin_users'))
    except: 
        return redirect(url_for('admin.admin_users'))
    return render_template('VerificationPassageAdmin.html')

@admin.route('/admin_remove_admin_confirm', methods = ["GET", "POST"])
@login_required
@admin_required 
def admin_remove_admin_confirm():
    try:
        user = session['login_to_be_removed_admin']
        if request.method == "POST":
            action = request.form['action']
            if action == "confirm":
                RemoveAdmin(user)
                return redirect(url_for('admin.admin_users'))
            if action == "abandon":
                return redirect(url_for('admin.admin_users'))
    except: 
        return redirect(url_for('admin.admin_users'))
    return render_template('VerificationDepassageAdmin.html')