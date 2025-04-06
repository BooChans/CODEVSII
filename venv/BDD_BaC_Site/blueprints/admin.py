from flask import Blueprint,render_template, redirect, url_for, request, flash,session
from ..functions.ModifMembres import ajouter_membre,get_profil,changer_mdp, confirm, changer_mdp_oublie
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from ..tools.models import Membres
from flask_session import Session
import datetime
from ..tools.decorators import logout_required, admin_required
from ..ttoken import generate_token, confirm_token
from ..mmail import send_email
from ..functions.admin_functions import add_one_bike,bike_list,remove_bike,user_list,MakeAdmin,remove_user,get_users,get_admin_users,get_admins,history,search_history,delete_history,RemoveAdmin,ModifStatutDanger, ModifStatutIndisponible,ModifStatutDisponible, userMessages, getMessage,messages, delMessage,getBookings,getSearchedBookings
from ..functions.reservations import supprimer_reservation


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
        elif action[0] == "abandon":
            return redirect(url_for('admin.admin_velos'))
        elif action[0] == "danger":
            ModifStatutDanger(action[1])
            return redirect(url_for('admin.admin_velos'))
        elif action[0] == "unavailable":
            ModifStatutIndisponible(action[1])
            return redirect(url_for('admin.admin_velos'))
        elif action[0] == "available":
            ModifStatutDisponible(action[1])
            return redirect(url_for('admin.admin_velos'))
    return render_template('AdminVelos.html',velos=velos, len_velos=len(velos), login= current_user.login, admin = current_user.is_admin)


@admin.route('/add_bike',methods=["GET","POST"])
@login_required
@admin_required
def add_bike():
    if request.method == "POST":
        hauteur = request.form['hauteur']
        longueur = request.form['longueur']
        statut = request.form['statut']
        if not hauteur or not longueur or not statut:
            flash("La taille et l'état sont nécéssaires")        
        else:
            add_one_bike(hauteur,longueur,statut)
            return redirect(url_for('admin.admin_tools'))
    return render_template('AjouterVelo.html', login=current_user.login, admin=current_user.is_admin)


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
    return render_template('ListeUtilisateurs.html', users=users, len_user=len(users), login=current_user.login, admin=current_user.is_admin)

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
    return render_template('ListeUtilisateurs.html', users=users, len_user=len(users),login=current_user.login, admin=current_user.is_admin)


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
            else: 
                session['search_date']=None
            return redirect(url_for('admin.admin_history'))
    return render_template('AdminHistorique.html', historique = historique, dh_historique=dh_historique, len_historique = len(historique),login=current_user.login, admin=current_user.is_admin)


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
                else: 
                    session['search_date']=None
                return redirect(url_for('admin.admin_search_history'))
    except: 
        return redirect(url_for('admin.admin_history'))
    return render_template('AdminHistorique.html', historique = historique, dh_historique=dh_historique, len_historique = len(historique),login=current_user.login, admin=current_user.is_admin)

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
    return render_template('VerificationSuppressionHistorique.html',login=current_user.login, admin=current_user.is_admin)

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
    return render_template('VerificationPassageAdmin.html',login=current_user.login, admin=current_user.is_admin)

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
                del session['login_to_be_removed']
                return redirect(url_for('admin.admin_users'))
            if action == "abandon":
                return redirect(url_for('admin.admin_users'))
    except: 
        return redirect(url_for('admin.admin_users'))
    return render_template('VerificationSuppressionUtilisateur.html',login=current_user.login, admin=current_user.is_admin)

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
    return render_template('VerificationDepassageAdmin.html',login=current_user.login, admin=current_user.is_admin)


@admin.route('/admin_messages', methods=["GET","POST"])
@login_required
@admin_required
def admin_messages():
    try: 
        messagees=userMessages(session['search_login_message'], session['search_date_message'])
    except:
        messagees=messages()
    if request.method == "POST":
        if request.form['action'] == 'search':
            session['search_login_message'] = request.form['login']
            if request.form['date']:
                date_list=request.form['date'].split("T")
                session['search_date_message']=date_list[0]+" 00:00:00"
            else: 
                session['search_date_message']=None
            return redirect(url_for('admin.admin_messages'))
    return render_template("ListeMessages.html", messages=messagees, len_messages=len(messagees),login=current_user.login, admin=current_user.is_admin)

@admin.route('/admin_message/<id_mes>', methods=["GET","POST"])
@admin_required
@login_required
def admin_message(id_mes):
    message = getMessage(id_mes)
    if request.method == 'POST':
        id_mes = request.form['delete']
        delMessage(id_mes)
        return redirect(url_for('admin.admin_messages'))
    return render_template("Message.html", message=message, login=current_user.login, admin=current_user.is_admin)        
            
@admin.route('/admin_bookings',methods=["GET","POST"])
@login_required
@admin_required                    
def admin_bookings():
    try: 
        bookings,dh_bookings = getSearchedBookings(session['search_login'],session['search_id_velo'],session['search_date'])
    except:
        bookings,dh_bookings = getBookings()
    if request.method == "POST":
        action = request.form['action'].split()
        if action[0] == 'search':
            session['search_login'] = request.form['login']
            session['search_id_velo'] = request.form['id_velo']
            if request.form['date']:
                date_list=request.form['date'].split("T")
                session['search_date']=date_list[0]+" 00:00:00"
            else: 
                session['search_date']=None
            return redirect(url_for('admin.admin_bookings'))
        if action[0] == 'delete':
            date_deb = action[2] + " " + action[3]
            id_membre = action[1]
            supprimer_reservation(id_membre,date_deb)
            return redirect(url_for('admin.admin_bookings'))
    return render_template('AdminReservations.html', historique = bookings, dh_historique=dh_bookings, len_historique = len(bookings),login=current_user.login, admin=current_user.is_admin)