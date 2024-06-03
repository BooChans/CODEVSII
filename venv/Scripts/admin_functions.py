import sqlite3
import datetime

def ModifEtatMembre(id_membre, etat):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Membres SET is_admin = ? WHERE id_membre = ?", (etat, id_membre))
    connection.commit()
    connection.close()
    
def MakeAdmin(id_membre):
    ModifEtatMembre(id_membre, True)

def RemoveAdmin(id_membre):
    ModifEtatMembre(id_membre, False)

def ModifStatutVelo(id_velo, statut):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Velos SET statut = ? WHERE id_velo = ?", (statut, id_velo))
    connection.commit()
    connection.close()

def ModifStatutDanger(id_velo):
    ModifStatutVelo(id_velo, "Danger")

def ModifStatutIndisponible(id_velo):
    ModifStatutVelo(id_velo, "Indisponible")

def ModifStatutDisponible(id_velo):
    ModifStatutVelo(id_velo,"Disponible")

def bike_list():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Velos")
    bikes=cur.fetchall()
    connection.close()
    return bikes

def user_list():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * from Membres")
    users=cur.fetchall()
    connection.close()
    return users

def deleteHistory():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique")
    connection.commit()
    connection.close()


def add_one_bike(hauteur,longueur,statut):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM Velos")
    c = cur.fetchone()[0]
    cur.execute('INSERT INTO Velos (id_velo,hauteur, longueur, statut) VALUES (?,?,?,?)', (c,hauteur,longueur,statut))
    connection.commit()
    connection.close()

def remove_bike(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE from Reservations where id_velo = ?", (id_velo,))
    cur.execute("DELETE from Historique where id_velo = ?", (id_velo,))
    cur.execute("DELETE from Velos where id_velo = ?",(id_velo,))
    connection.commit()
    connection.close()

def update_bike(id_velo, hauteur, longueur, statut):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    if not id_velo:
        cur.execute("UPDATE Velos SET hauteur = ?, longueur = ?, statut = ? where id_velo = ?", (hauteur,longueur,statut,id_velo))

def remove_user(id_membre):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE from Messages where id_membre = ?",(id_membre,))
    cur.execute("DELETE from Reservations where id_membre = ?", (id_membre,))
    cur.execute("DELETE from Historique where id_membre = ?", (id_membre,))
    cur.execute("DELETE from Membres where id_membre = ?",(id_membre,))
    connection.commit()
    connection.close()

def get_users(login):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * from Membres where login LIKE '{login}%'".format(login=login)
    cur.execute(query)
    users = cur.fetchall()
    connection.close()
    return users

def get_admin_users(login):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * from Membres where login LIKE '{login}%' and is_admin = 1".format(login=login)
    cur.execute(query)
    users = cur.fetchall()
    connection.close()
    return users

def get_admins():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * from Membres WHERE is_admin = 1"
    cur.execute(query)
    users = cur.fetchall()
    connection.close()
    return users

def history():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre"
    cur.execute(query)
    history = cur.fetchall()
    dh_history = [(datetime.datetime.strptime(history[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(history[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(history[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(history[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(history))]
    connection.close()
    return history,dh_history


def search_history(login, id_velo, date):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    if date: 
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_lendemain = date + datetime.timedelta(days = 1)
    if not login and not id_velo and not date:
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre"
        cur.execute(query)
        history = cur.fetchall()
    if login and not id_velo and not date:
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where login = ?"
        cur.execute(query,(login,))
        history = cur.fetchall()
    if id_velo and not login and not date:
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where id_velo = ?"
        cur.execute(query,(id_velo,))
        history = cur.fetchall()
    if date and not login and not id_velo:
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where date_deb > ? and date_deb < ?"
        cur.execute(query, (date,date_lendemain))
        history = cur.fetchall()
    if login and id_velo and not date: 
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where login = ? and id_velo = ?"
        cur.execute(query, (login, id_velo))
        history = cur.fetchall()
    if login and not id_velo and date: 
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where login = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (login, date,date_lendemain))
        history = cur.fetchall()
    if not login and id_velo and date: 
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where id_velo = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (id_velo, date,date_lendemain))
        history = cur.fetchall()
    if login and id_velo and date: 
        query = "SELECT * from Membres M join Historique H on M.id_membre = H.id_membre where login = ? and id_velo = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (login ,id_velo, date,date_lendemain))
        history = cur.fetchall()
    dh_history = [(datetime.datetime.strptime(history[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(history[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(history[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(history[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(history))]
    connection.close()
    return history,dh_history

def delete_history():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "DELETE from Historique"
    cur.execute(query)
    connection.commit()
    connection.close()

def messages():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre order by M.date desc"
    cur.execute(query)
    messagees = cur.fetchall()
    connection.close()
    return messagees

def userMessages(id_membre, date):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    if date: 
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_lendemain = date + datetime.timedelta(days = 1)
    if not id_membre and not date: 
        query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre order by M.date desc"
        cur.execute(query)
    elif id_membre and not date:
        query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre where M.login = ? M.date desc"
        cur.execute(query, (id_membre,))
    elif not id_membre and date: 
        query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre where M.date > ? and M.date < ? M.date desc"
        cur.execute(query, (date,date_lendemain))   
    elif id_membre and date: 
        query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre where M.date > ? and M.date < ? and M.login = ? M.date desc"
        cur.execute(query, (date,date_lendemain,id_membre))              
    messagees = cur.fetchall()
    connection.close()
    return messagees

def getMessage(id_mes):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * FROM Messages M join Membres F on M.id_membre = F.id_membre where id_mes = ?"
    cur.execute(query, (id_mes,))
    message = cur.fetchone()
    connection.close()
    return message

def delMessage(id_mes):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "DELETE FROM Messages where id_mes = ?"
    cur.execute(query,(id_mes,))
    connection.commit()
    connection.close()

def getBookings():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    query = "SELECT * FROM Reservations R join Membres F on R.id_membre = F.id_membre"
    cur.execute(query)
    bookings = cur.fetchall()
    connection.close()
    dh_bookings = [(datetime.datetime.strptime(bookings[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(bookings[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(bookings[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(bookings[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(bookings))]
    return bookings,dh_bookings

def getSearchedBookings(login, id_velo, date):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    if date: 
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date_lendemain = date + datetime.timedelta(days = 1)
    if not login and not id_velo and not date:
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre"
        cur.execute(query)
    if login and not id_velo and not date:
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where login = ?"
        cur.execute(query,(login,))
    if id_velo and not login and not date:
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where id_velo = ?"
        cur.execute(query,(id_velo,))
    if date and not login and not id_velo:
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where date_deb > ? and date_deb < ?"
        cur.execute(query, (date,date_lendemain))
    if login and id_velo and not date: 
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where login = ? and id_velo = ?"
        cur.execute(query, (login, id_velo))
    if login and not id_velo and date: 
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where login = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (login, date,date_lendemain))
    if not login and id_velo and date: 
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where id_velo = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (id_velo, date,date_lendemain))
    if login and id_velo and date: 
        query = "SELECT * from Membres M join Reservations H on M.id_membre = H.id_membre where login = ? and id_velo = ? and date_deb > ? and date_deb < ?"
        cur.execute(query, (login ,id_velo, date,date_lendemain))
    bookings = cur.fetchall()
    dh_bookings = [(datetime.datetime.strptime(bookings[i]['date_deb'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(bookings[i]['date_deb'],'%Y-%m-%d %X').time(),datetime.datetime.strptime(bookings[i]['date_fin'],'%Y-%m-%d %X').date(),datetime.datetime.strptime(bookings[i]['date_fin'],'%Y-%m-%d %X').time()) for i in range(len(bookings))]
    connection.close()
    return bookings,dh_bookings