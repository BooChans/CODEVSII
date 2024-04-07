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
    cur.execute("SELECT COUNT(id_res) FROM reservations")
    c = cur.fetchone()
    code = generate_unique_code()
    cur.execute("SELECT date_fin FROM reservations WHERE id_velo=?", (id_velo,))
    result = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM reservations WHERE id_velo=?", (id_velo,))
    n = cur.fetchone()[0]
    b = True
    for i in range(n) : b = b and result[i] > date_deb_dt.strftime('%Y-%m-%d') 
    if result and b:
        print(f"Ce vélo est réservé à cette date")
    else:
        cur.execute("INSERT INTO reservations (id_res, id_membre, id_velo, date_deb, date_fin, code) VALUES (?, ?, ?, ?, ?, ?)",
                (c[0]+1, id_membre, id_velo, date_deb, date_fin.strftime('%Y-%m-%d'), code))
        connection.commit()
# le code de reservation pêrmet tjrs de reserver 2 fois le meme velo meme journée
def supprimer_reservations_date_depassee():
    # Obtenez la date actuelle
    date_actuelle = datetime.date.today().strftime('%Y-%m-%d')
    
    # Supprimez les réservations avec une date de fin inférieure à la date actuelle
    cur.execute("DELETE FROM reservations WHERE date_fin < ?", (date_actuelle,))
    connection.commit()

# Appelez cette fonction pour supprimer les réservations dépassées
supprimer_reservations_date_depassee()

reserver_velo(1, 1, '2024-04-09')
reserver_velo(2,2, '2024-04-09')
