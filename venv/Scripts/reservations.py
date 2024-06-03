import sqlite3
import flask
import random
import datetime
from .exceptions import Reservationdejaprise,Dejareserve

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

def generate_unique_code():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    while True:
        code = random.randint(1000, 9999)
        cur.execute("SELECT COUNT(*) FROM reservations WHERE code = ?", (code,))
        if cur.fetchone()[0] == 0:
            connection.close()
            return code


def reserver_velo(id_velo, id_membre, date_deb,date_end):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()

    
    cur.execute("SELECT COUNT(*) FROM reservations WHERE id_velo = ? AND date_fin > ? AND date_deb < ?", (id_velo, date_deb, date_end))
    num_overlapping_reservations = cur.fetchone()[0]
    
    if num_overlapping_reservations > 0:
        print("Ce vélo est déjà réservé pour cette période")
        connection.close()
        Dejareserve()
    else:
        cur.execute("SELECT COUNT(*) FROM reservations WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
        num_booking = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM reservations WHERE id_membre = ?", (id_membre,))
        num_bookuser = cur.fetchone()[0]
        if num_booking == 0 and num_bookuser < 2: 
            cur.execute("INSERT INTO Historique ( id_membre, id_velo, date_deb, date_fin) VALUES ( ?, ?, ?, ?)",
                        (id_membre, id_velo,  date_deb, date_end))
            code = generate_unique_code()
            cur.execute("INSERT INTO Reservations ( id_membre, id_velo, code, date_deb, date_fin) VALUES ( ?, ?, ?, ?, ?)",
                        (id_membre, id_velo, code,  date_deb,date_end))
            connection.commit()
            connection.close()
        else: 
            connection.close()
            Reservationdejaprise(id_membre)

            

def velos_disponibles(date_deb,date_fin):

    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row

    
    cur.execute("""SELECT * FROM Velos WHERE statut = 'Disponible' and id_velo NOT IN (
            SELECT id_velo
            FROM reservations
            WHERE date_fin > ? AND date_deb < ?
        )""", (date_deb, date_fin))
    
    velos_disponibles = cur.fetchall()
    
    if velos_disponibles:
        print("Vélos disponibles pour la date:", date_deb)
        velos =[]
        for velo in velos_disponibles:
            if velo[0] not in velos :
                velos.append(velo)  
        connection.close()
        return velos
    else:
        print("Aucun vélo disponible pour la date:", date_deb)
        connection.close()
        return []


def supprimer_reservations_date_depassee():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
   
    date_actuelle = datetime.datetime.now().strftime('%Y-%m-%d %X')
    print(date_actuelle)
    
    cur.execute("DELETE FROM Reservations WHERE date_fin < ?", (date_actuelle,))
    connection.commit()
    connection.close()

def supprimer_reservation(id_membre,date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
    cur.execute("DELETE FROM Reservations WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
    connection.commit()
    connection.close()

def afficher_code(id_membre,date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT code from Reservations WHERE id_membre = ? and date_deb = ?",(id_membre,date_deb))
    code_booking=cur.fetchone()[0]
    connection.close()
    return code_booking

def velo_est_disponible(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT statut FROM Velos WHERE id_velo = ?", (id_velo))
    b = cur.fetchone()[0]
    connection.close()
    return b == 'Disponible'


def reservationsencours(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Reservations WHERE id_membre = ?",(id_membre,))
    bookings=cur.fetchall()
    connection.close()
    return bookings


def afficher_historique_user(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Historique WHERE id_membre = ? ORDER by date_deb DESC",(id_membre,))
    history_all=cur.fetchall()
    cur.execute("SELECT * from Historique H where id_membre = ? and not exists(SELECT * from Reservations R where R.id_membre = H.id_membre and R.id_velo = H.id_velo and R.date_deb = H.date_deb)", (id_membre,))
    history_done = cur.fetchall()
    connection.close()
    return history_all,history_done


def afficher_historique_bike(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Historique WHERE id_velo = ?",(id_velo,))
    history_b=cur.fetchall()
    connection.close()
    return history_b

def codes_list():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT id_velo,code,date_deb from Reservations")
    codes=cur.fetchall()
    connection.close()
    return [(code['id_velo'],code['code'], code['date_deb']) for code in codes]

def tableau_de_bord(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Historique H join Velos V on H.id_velo = V.id_velo where id_membre = ? order by date_deb", (id_membre,))
    historique = cur.fetchmany(3)
    dh_historique = [(datetime.datetime.strptime(historique[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(historique[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(historique[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(historique[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(historique))]

    cur.execute("SELECT * from Reservations R join Velos V on R.id_velo = V.id_velo where id_membre = ? order by date_deb", (id_membre,))
    reservations = cur.fetchmany(2)
    connection.close()
    dh_reservations = [(datetime.datetime.strptime(reservations[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(reservations[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(reservations[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(reservations[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(reservations))]
    return historique,dh_historique,reservations,dh_reservations

def bikes():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM Velos")
    velos = cur.fetchall()
    connection.close()
    return velos

def given_back(id_membre, id_velo, date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    date_actuelle = datetime.datetime.now().strftime('%Y-%m-%d %X')
    cur.row_factory = sqlite3.Row
    cur.execute("UPDATE set date_remise = ? where id_velo = ? and id_velo = ? and date_deb = ?" (date_actuelle,id_membre, id_velo,date_deb))
    connection.close()

def countNonGivenBack(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT COUNT(*) from Historique H where id_membre = ? and not exists(SELECT * from Reservations R where R.id_membre = H.id_membre and R.id_velo = H.id_velo and R.date_deb = H.date_deb)", (id_membre,))
    count = cur.fetchone()[0]
    connection.close()
    return count

