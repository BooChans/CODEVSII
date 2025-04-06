import sqlite3

connection = sqlite3.connect('BDD_velos.db')


cur = connection.cursor()


cur.execute("INSERT INTO Velos (id_velo,hauteur,longueur, disponibilite) VALUES (?,?,?,?)",
            (10,130,140,False))

connection.commit()
connection.close()