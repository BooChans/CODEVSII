from flask import Blueprint,render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .models import Membres
from .reservations import velos_disponibles,supprimer_reservations_date_depassee, reserver_velo,supprimer_reservation,afficher_code
from flask_session import Session

booking = Blueprint('booking', __name__)

@booking.route('/available', methods=['GET','POST'])
def available():
    if request.method == 'POST':
        date=request.form['date']
        session['date']=date
        supprimer_reservations_date_depassee()
        velos=velos_disponibles(date)
        adress_list=[url_for('main.index')+str(velos[i]['id_velo']) for i in range(len(velos))]
        return render_template('index.html', len=len(velos), velos=velos, adress_list=adress_list)
    return render_template('date_picker.html')

@booking.route('/book')
def book():
    reserver_velo(session['velo'],current_user.id_membre,session['date'])
    return 'OK'

@booking.route('/bookcancel')
def bookcancel():
    supprimer_reservation(current_user.id_membre,session['date'])
    return('Suppression OK')




