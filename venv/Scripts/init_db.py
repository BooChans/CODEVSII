import sqlite3

connection = sqlite3.connect('BDD_velos.db')


with open('test.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

cur.execute("INSERT INTO Velos (id_velo,hauteur,longueur, disponibilite) VALUES (?,?,?,?)",
            (10,130,140,False))

connection.commit()
connection.close()