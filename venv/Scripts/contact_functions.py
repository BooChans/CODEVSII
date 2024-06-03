import sqlite3
import datetime

def putMessage(id_membre, message,titre , type):
    date_actuelle = datetime.datetime.now().strftime('%Y-%m-%d %X')
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.row_factory = sqlite3.Row
    cur.execute("INSERT INTO Messages (id_membre,date,message,titre ,type) VALUES (?,?,?,?,?)",(id_membre,date_actuelle,message,titre,type))
    connection.commit()
    connection.close()

