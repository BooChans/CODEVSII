import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint,session
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash,check_password_hash
import socket
from ..functions.ModifMembres import ajouter_membre, get_profil
from flask_login import current_user
from flask_session import Session
from ..functions.reservations import reserver_velo,supprimer_reservation,afficher_code,supprimer_reservations_date_depassee,velos_disponibles,tableau_de_bord,bikes
import datetime
from ..tools.models import Membres
from ..tools.decorators import admin_required


main = Blueprint('main', __name__)


UDP_IP = "127.0.0.1"
UDP_PORT = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   



def get_db_connection():
    conn = sqlite3.connect('BDD_velos.db')
    con = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(id_velo):
    conn = get_db_connection()
    velo = conn.execute('SELECT * FROM Velos WHERE id_velo = ?',
                        (id_velo,)).fetchone()
    conn.close()
    if velo is None:
        abort(404)
    return velo




@main.route('/')
def index():
    #conn = get_db_connection()
    #velos = conn.execute('SELECT * FROM Velos').fetchall()
    #conn.close()
    #adress_list=[url_for('main.index')+str(velos[i]['id_velo']) for i in range(len(velos))]

    try: 
        user = current_user.login
        admin = current_user.is_admin
    except: 
        user = None
        admin = False
    return render_template('Accueil.html',login=user, admin=admin)

@main.route('/<int:post_id>',methods=['GET','POST'])
def post(post_id):
    velo = get_post(post_id)
    if request.method == "POST":
        action = request.form['action'].split()
        if action[0] == "book":
            try: 
                reserver_velo(action[1],current_user.id_membre, action[2])
                return render_template('success_book.html',date=action[2])
            except:
                return redirect(url_for('main.index'))
    return render_template('page_information_velo.html', velo=velo)
    

@main.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('main.index'))    
    return render_template('create.html')

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/add_member',methods=('GET','POST'))
def add_member():
    if request.method == 'POST':
        login = request.form['login']
        mdp = request.form['mdp']
        mail = request.form['mail']
        phone_number = request.form['phone_number']
        if not login:
            flash('login est nécéssaire')        
        else:
            try:
                ajouter_membre(login,mdp,mail)
                return redirect(url_for('main.index'))
            except: 
                flash('nope')

    return render_template('aj_membres.html')

@main.route('/velos')
def velos():
    try: 
        login=current_user.login
        is_admin = current_user.is_admin
    except: 
        login = None
        is_admin = None
    velos = bikes()
    return render_template('Velos.html',velos=velos, len_velos=len(velos), login=login, admin=is_admin)


@main.route('/profil', methods=('GET','POST'))
def show_profil():
        profil = get_profil(current_user.login)
        return render_template('aff_prof.html', profil=profil)

@main.route('/profile',methods=['GET','POST'])
@admin_required
def profile():
    #try: 

    historique,dh_historique,reservations,dh_reservations = tableau_de_bord(current_user.id_membre)
    if request.method == 'POST':
        action = request.form['action']
        date_deb=request.form['date_deb']
        date_fin = request.form['date_fin']
        if not date_deb or not date_fin:
            if action[0] == "remove":
                supprimer_reservation(current_user.id_membre, action[1]+" "+action[2])
                return render_template('booking_removed.html',date=action[1]+" "+action[2])
            elif action[0] == "see_code":
                code = afficher_code(current_user.id_membre,action[1]+" "+action[2])
                return render_template('code.html',code=code)
        elif date_deb and date_fin:
            date_deb_list=request.form['date_deb'].split("T")
            date_fin_list=request.form['date_fin'].split("T")
            date_deb=" ".join(date_deb_list)+":00"
            date_fin= " ".join(date_fin_list)+":00"
            session['date_deb']=date_deb
            session['date_fin']=date_fin
            supprimer_reservations_date_depassee()
            velos=velos_disponibles(session['date_deb'],session['date_fin'])
            print(velos,len(velos))
            return render_template('Tableau_de_bord.html', login=current_user.login, mail=current_user.mail,numero_tel=current_user.numero_tel, velos=velos,len=0, step2=True, len_historique=len(historique),historique=historique, reservations=reservations, len_reservations=len(reservations),dh_historique=dh_historique,dh_reservations=dh_reservations,len_velos=len(velos))
        return redirect(url_for('booking.book'))
    return render_template('Tableau_de_bord.html', login=current_user.login, mail=current_user.mail,numero_tel=current_user.numero_tel, velos=[],len=0, step2=False, len_historique=len(historique),historique=historique, reservations=reservations, len_reservations=len(reservations),dh_historique=dh_historique,dh_reservations=dh_reservations,len_velos=0)
    #except: 
        #return redirect(url_for('auth.login'))
        