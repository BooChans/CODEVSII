import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
import socket

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hi'


@app.route('/')
def index():
    conn = get_db_connection()
    velos = conn.execute('SELECT * FROM Velos').fetchall()
    conn.close()
    adress_list=["http://127.0.0.1:5000/"+str(velos[i]['id_velo']) for i in range(len(velos))]
    return render_template('index.html', len=len(velos), velos=velos, adress_list=adress_list)

@app.route('/<int:post_id>')
def post(post_id):
    velo = get_post(post_id)
    return render_template('page_information_velo.html', velo=velo)

@app.route('/create', methods=('GET', 'POST'))
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
            return redirect(url_for('index'))    
    return render_template('create.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add_velo', methods = ('GET','POST'))
def add_velo():
    if request.method == 'POST':
        id_velo = int(request.form['id_velo'])
        hauteur = int(request.form['hauteur'])
        longueur = int(request.form['longueur'])
        if not id_velo:
            flash('id_vélo est nécéssaire')
        
        else:
            try:
                conn = get_db_connection()
                conn.execute('INSERT INTO Velos (id_velo,hauteur, longueur, disponibilite) VALUES (?,?,?,?)', (id_velo,hauteur,longueur,True))
                conn.commit()
                conn.close()
                s.sendto(bytes(f"Le vélo {id_velo} a été ajouté, de hauteur {hauteur} et de longueur {longueur}","utf-8"), (UDP_IP, UDP_PORT))
                return redirect(url_for('index'))
            except:
                flash('nope')
    return render_template('aj_velo.html')
