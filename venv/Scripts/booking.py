from flask import Blueprint,render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user,login_required
from .models import Membres
from .reservations import velos_disponibles,supprimer_reservations_date_depassee, reserver_velo,supprimer_reservation,afficher_code,reservationsencours,afficher_historique_user,codes_list,tableau_de_bord,afficher_code
from flask_session import Session
from .decorators import confirmed_required
import socket

UDP_PC = "192.168.43.84"
UDP_PORT = 2390
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP   

booking = Blueprint('booking', __name__)

@booking.route('/available', methods=['GET','POST'])
@login_required
def available():
    if request.method == 'POST':
        date_deb_list=request.form['date_deb'].split("T")
        date_fin_list=request.form['date_fin'].split("T")
        date_deb=" ".join(date_deb_list)+":00"
        date_fin= " ".join(date_fin_list)+":00"
        print(date_deb,date_fin)
        session['date_deb']=date_deb
        session['date_fin']=date_fin
        supprimer_reservations_date_depassee()
        return redirect(url_for('booking.book'))
    return render_template('date_picker.html')



@booking.route('/book',methods=['POST','GET'])
@login_required
def book():
    velos=velos_disponibles(session['date_deb'],session['date_fin'])
    if request.method == 'POST':
        action=request.form['action'].split()
        if action[0] == "book":
            try:
                reserver_velo(action[1],current_user.id_membre, action[2]+" "+action[3],action[4]+" "+action[5])
                codes=codes_list()
                print(codes)
                for code in codes:
                    s.sendto(bytes(str(code[0])+" "+str(code[1]),'utf-8'),(UDP_PC,UDP_PORT))
                return render_template('success_book.html',date=action[2])
            except:
                flash("Le vélo choisi est déjà réservé pour la période choisie")
                return redirect(url_for('booking.available'))
    return render_template('index_booking.html', len=len(velos), velos=velos, date_deb=session['date_deb'],date_fin=session['date_fin'])

@booking.route('/bookcancel')
@login_required
def bookcancel():
    supprimer_reservation(current_user.id_membre,session['date'])
    return('Suppression OK')


@booking.route('/bookings',methods=['GET','POST'])
@login_required
def bookings():
    supprimer_reservations_date_depassee()
    bookings=reservationsencours(current_user.id_membre)
    if request.method == 'POST':
        codes=codes_list()
        for code in codes:
            s.sendto(bytes(str(code[0])+" "+str(code[1]),'utf-8'),(UDP_PC,UDP_PORT))
        action = request.form['action'].split()
        if action[0] == "remove":
             supprimer_reservation(current_user.id_membre, action[1]+" "+action[2])
             return render_template('booking_removed.html',date=action[1]+" "+action[2])
        elif action[0] == "see_code":
             code = afficher_code(current_user.id_membre,action[1]+" "+action[2])
             return render_template('code.html',code=code)
    return render_template('bookings.html', bookings=bookings, len=len(bookings))

@booking.route('/history_user', methods=['GET'])
@login_required
def history_user():
    history_u=afficher_historique_user(current_user.id_membre)
    return render_template('bookings.html',bookings=history_u,len=len(history_u))


@booking.route('/dashboard',methods=['GET','POST'])
@login_required
@confirmed_required
def dashboard():
    #try: 
    supprimer_reservations_date_depassee() #print la date
    historique,dh_historique,reservations,dh_reservations = tableau_de_bord(current_user.id_membre)
    codes=codes_list()
    print(codes)
    for code in codes:
        s.sendto(bytes(str(code[0])+" "+str(code[1]),'utf-8'),(UDP_PC,UDP_PORT))
    if request.method == 'POST':
        actions = request.form
        if 'action' in actions:
            action = actions['action'].split()
        if 'date_deb' in actions and 'date_fin' in actions:
            date_deb_form = actions['date_deb']
            date_fin_form = actions['date_fin']  
        else: 
            date_deb_form = None
            date_fin_form = None
        if 'book' in actions:
            id_velo = int(actions['book']) 
            try: 
                reserver_velo(id_velo,current_user.id_membre, session['date_deb'],session['date_fin'])
                return render_template('success_book.html',date=session['date_deb'])
            except: 
                flash("Vélo réservé à cette date ou vous avez déjà deux réservations actives")
                return redirect(url_for('booking.dashboard'))
        if not date_deb_form or not date_fin_form:
            if action[0] == "remove":
                supprimer_reservation(current_user.id_membre, action[1]+" "+action[2])
                return render_template('booking_removed.html',date=action[1]+" "+action[2])
            elif action[0] == "see_code":

                code = afficher_code(current_user.id_membre,action[1]+" "+action[2])
                return render_template('code.html',code=code)
        elif date_deb_form and date_fin_form:
            date_deb_list=date_deb_form.split("T")
            date_fin_list=date_fin_form.split("T")
            date_deb=" ".join(date_deb_list)+":00"
            date_fin= " ".join(date_fin_list)+":00"
            session['date_deb']=date_deb
            session['date_fin']=date_fin
            supprimer_reservations_date_depassee()
            velos=velos_disponibles(session['date_deb'],session['date_fin'])
            return render_template('Tableau_de_bord.html', login=current_user.login, mail=current_user.mail,numero_tel=current_user.numero_tel, velos=velos, step2=True, len_historique=len(historique),historique=historique, reservations=reservations, len_reservations=len(reservations),dh_historique=dh_historique,dh_reservations=dh_reservations,len_velos=len(velos)) 
        return render_template('Tableau_de_bord.html', login=current_user.login, mail=current_user.mail,numero_tel=current_user.numero_tel, velos=[],len=0, step2=False, len_historique=len(historique),historique=historique, reservations=reservations, len_reservations=len(reservations),dh_historique=dh_historique,dh_reservations=dh_reservations,len_velos=0)
    return render_template('Tableau_de_bord.html', login=current_user.login, mail=current_user.mail,numero_tel=current_user.numero_tel, velos=[],len=0, step2=False, len_historique=len(historique),historique=historique, reservations=reservations, len_reservations=len(reservations),dh_historique=dh_historique,dh_reservations=dh_reservations,len_velos=0)
    #except: 
        #return redirect(url_for('auth.login'))
        
@booking.route('/history')
@login_required
def history():
    userHistory = afficher_historique_user(current_user.id_membre)
    return render_template('Historique.html', userHistory=userHistory,len_userHistory = len(userHistory))