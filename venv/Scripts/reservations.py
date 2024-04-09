import sqlite3
import flask
import random
import datetime

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

def generate_unique_code():
    while True:
        code = random.randint(1000, 9999)
        cur.execute("SELECT COUNT(*) FROM reservations WHERE code = ?", (code,))
        if cur.fetchone()[0] == 0:
            return code

def reserver_velo(id_velo, id_membre, date_deb):
    date_deb_dt = datetime.datetime.strptime(date_deb, '%Y-%m-%d')
    date_fin = date_deb_dt + datetime.timedelta(days=1)
    
    cur.execute("SELECT COUNT(*) FROM reservations WHERE id_velo = ? AND date_fin > ? AND date_deb < ?", (id_velo, date_deb, date_fin))
    num_overlapping_reservations = cur.fetchone()[0]
    
    if num_overlapping_reservations > 0:
        print("Ce vélo est déjà réservé pour cette période")
    else:
        code = generate_unique_code()
        cur.execute("INSERT INTO reservations ( id_membre, id_velo, date_deb, date_fin, code) VALUES ( ?, ?, ?, ?, ?)",
                    (id_membre, id_velo, date_deb, date_fin.strftime('%Y-%m-%d'), code))
        connection.commit()

def velos_disponibles(date_deb):
    date_deb_dt = datetime.datetime.strptime(date_deb, '%Y-%m-%d')
    date_fin = date_deb_dt + datetime.timedelta(days=1)
    
    cur.execute("""
        SELECT id_velo
        FROM Velos
        WHERE id_velo NOT IN (
            SELECT id_velo
            FROM reservations
            WHERE date_fin >= ? AND date_deb <= ?
        )
    """, (date_deb, date_fin))
    
    velos_disponibles = cur.fetchall()
    
    if velos_disponibles:
        print("Vélos disponibles pour la date:", date_deb)
        velos =[]
        for velo in velos_disponibles:
            if velo[0] not in velos :
                velos.append(velo[0])  
        print(velos)
    else:
        print("Aucun vélo disponible pour la date:", date_deb)


def supprimer_reservations_date_depassee():
   
    date_actuelle = datetime.date.today().strftime('%Y-%m-%d')
    
    cur.execute("DELETE FROM reservations WHERE date_fin < ?", (date_actuelle,))
    connection.commit()

supprimer_reservations_date_depassee()

reserver_velo(1, 1, '2024-05-09')
reserver_velo(2,2, '2024-05-09')
velos_disponibles('2024-05-09')
velos_disponibles('2024-07-09')

