import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, Blueprint,session
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash,check_password_hash
import socket
from .ModifMembres import ajouter_membre, get_profil
from flask_login import current_user
from flask_session import Session


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
    conn = get_db_connection()
    velos = conn.execute('SELECT * FROM Velos').fetchall()
    conn.close()
    adress_list=[url_for('main.index')+str(velos[i]['id_velo']) for i in range(len(velos))]
    return render_template('index.html', len=len(velos), velos=velos, adress_list=adress_list)

@main.route('/<int:post_id>')
def post(post_id):
    velo = get_post(post_id)
    return render_template('page_information_velo.html', velo=velo)

@main.route('/<int:post_id>', methods=['POST'])
def post_post(post_id):
    velo = get_post(post_id)

    if request.method == 'POST':
        print("hi2")
        session['velo']=velo['id_velo']
        return redirect(url_for('booking.book'))
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

@main.route('/add_velo', methods = ('GET','POST'))
def add_velo():
    if request.method == 'POST':
        hauteur = int(request.form['hauteur'])
        longueur = int(request.form['longueur'])
        if not hauteur and not longueur:
            flash('la taille est nécéssaire')
        
        else:
            
            conn = get_db_connection()
            c= conn.cursor().execute("SELECT COUNT(*) FROM Velos").fetchone()
            print(c)
            conn.execute('INSERT INTO Velos (id_velo,hauteur, longueur, disponibilite) VALUES (?,?,?,?)', (c[0]+1000,hauteur,longueur,True))
            conn.commit()
            conn.close()
            s.sendto(bytes(f"Le vélo {c[0]+1000} a été ajouté, de hauteur {hauteur} et de longueur {longueur}","utf-8"), (UDP_IP, UDP_PORT))
            return redirect(url_for('main.index'))

    return render_template('aj_velo.html')

@main.route('/add_member',methods=('GET','POST'))
def add_member():
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
                flash('nope')

    return render_template('aj_membres.html')

@main.route('/profil', methods=('GET','POST'))
def show_profil():
    if request.method == 'POST': 
        login=request.form['login']
        profil = get_profil(login)
        if profil is not None:
            return render_template('aff_prof.html', profil=profil)
        else: 
            abort(404)
    return render_template('dem_log.html')

@main.route('/profile')
def profile():
    try: 
        return render_template('aff_profile.html', login=current_user.login, mail=current_user.mail)
    except: 
        return redirect(url_for('auth.login'))