import sqlite3
import flask
import random
import datetime
from .exceptions import Reservationdejaprise

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

def generate_unique_code():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    while True:
        code = random.randint(1000, 9999)
        cur.execute("SELECT COUNT(*) FROM reservations WHERE code = ?", (code,))
        if cur.fetchone()[0] == 0:
            return code

def reserver_velo(id_velo, id_membre, date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    date_deb_dt = datetime.datetime.strptime(date_deb, '%Y-%m-%d')
    date_fin = date_deb_dt + datetime.timedelta(days=1)
    
    cur.execute("SELECT COUNT(*) FROM reservations WHERE id_velo = ? AND date_fin > ? AND date_deb < ?", (id_velo, date_deb, date_fin))
    num_overlapping_reservations = cur.fetchone()[0]
    
    if num_overlapping_reservations > 0:
        print("Ce vélo est déjà réservé pour cette période")
    else:
        cur.execute("SELECT COUNT(*) FROM reservations WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
        num_booking = cur.fetchone()[0]
        if num_booking == 0: 
            cur.execute("INSERT INTO Historique ( id_membre, id_velo, date_deb, date_fin) VALUES ( ?, ?, ?, ?, ?)",
                        (id_membre, id_velo,  date_deb, date_fin.strftime('%Y-%m-%d')))
            code = generate_unique_code()
            cur.execute("INSERT INTO Reservations ( id_membre, id_velo, code, date_deb, date_fin) VALUES ( ?, ?, ?, ?, ?)",
                        (id_membre, id_velo, code,  date_deb, date_fin.strftime('%Y-%m-%d')))
            connection.commit()
        else: 
            Reservationdejaprise(id_membre)
            

def velos_disponibles(date_deb):

    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    date_deb_dt = datetime.datetime.strptime(date_deb, '%Y-%m-%d')
    date_fin = date_deb_dt + datetime.timedelta(days=1)
    
    cur.execute("""
        SELECT * FROM Velos
        WHERE statut = 'Disponible'
        )
    """, (date_deb, date_fin))
    
    velos_disponibles = cur.fetchall()
    
    if velos_disponibles:
        print("Vélos disponibles pour la date:", date_deb)
        velos =[]
        for velo in velos_disponibles:
            if velo[0] not in velos :
                velos.append(velo)  
        return velos
    else:
        print("Aucun vélo disponible pour la date:", date_deb)


def supprimer_reservations_date_depassee():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
   
    date_actuelle = datetime.date.today().strftime('%Y-%m-%d')
    
    cur.execute("DELETE FROM reservations WHERE date_fin < ?", (date_actuelle,))
    connection.commit()

def supprimer_reservation(id_membre,date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
    cur.execute("DELETE FROM Reservations WHERE id_membre = ? and date_deb = ?", (id_membre,date_deb))
    connection.commit()

def afficher_code(id_membre,date_deb):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT code from Reservations WHERE id_membre = ? and date_deb = ?",(id_membre,date_deb))
    code_booking=cur.fetchone()[0]
    return code_booking

def velo_est_disponible(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT statut FROM Velos WHERE id_velo = ?", (id_velo))
    b = cur.fetchone()[0]
    return b == 'Disponible'


def reservationsencours(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Reservations WHERE id_membre = ?",(id_membre,))
    bookings=cur.fetchall()
    return bookings
