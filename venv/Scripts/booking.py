from flask import Blueprint,render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from .models import Membres
from .reservations import velos_disponibles,supprimer_reservations_date_depassee, reserver_velo,supprimer_reservation,afficher_code,reservationsencours
from flask_session import Session

booking = Blueprint('booking', __name__)

@booking.route('/available', methods=['GET','POST'])
def available():
    if request.method == 'POST':
        date=request.form['date']
        session['date']=date
        supprimer_reservations_date_depassee()
        return redirect(url_for('booking.book'))
    return render_template('date_picker.html')



@booking.route('/book',methods=['POST','GET'])
def book():
    velos=velos_disponibles(session['date'])
    if request.method == 'POST':
        action=request.form['action'].split()
        if action[0] == "book":
            try: 
                reserver_velo(action[1],current_user.id_membre, action[2])
                return render_template('success_book.html',date=action[2])
            except:
                return redirect(url_for('main.index'))
    return render_template('index_booking.html', len=len(velos), velos=velos, date=session['date'])

@booking.route('/bookcancel')
def bookcancel():
    supprimer_reservation(current_user.id_membre,session['date'])
    return('Suppression OK')


@booking.route('/bookings',methods=['GET','POST'])
def bookings():
    bookings=reservationsencours(current_user.id_membre)
    if request.method == 'POST':
        action = request.form['action'].split()
        if action[0] == "remove":
             supprimer_reservation(current_user.id_membre, action[1])
             return render_template('booking_removed.html',date=action[1])
        elif action[0] == "see_code":
             code = afficher_code(current_user.id_membre,action[1])
             return render_template('code.html',code=code)
    return render_template('bookings.html', bookings=bookings, len=len(bookings))