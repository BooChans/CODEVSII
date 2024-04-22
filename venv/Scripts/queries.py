import sqlite3
import datetime
from werkzeug.security import generate_password_hash, check_password_hash


connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

date=datetime.datetime.now().strftime('%Y-%m-%d %X')
#cur.execute("""INSERT INTO Membres
#            (id_membre, login, password, mail, numero_tel,
#            is_admin, is_confirmed, registered_on, confirmed_on) VALUES (?,?,?,?,?,?,?,?,?)""",(0, "admin_BDD", generate_password_hash("114admin"),"@BDD.com",0000000000, True, True, date, date))

cur.execute("DELETE FROM Velos where id_velo = ?", (0,))
connection.commit()