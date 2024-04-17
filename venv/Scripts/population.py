import sqlite3

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()


cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('amer','bla1','amer@example.com', '0763585487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('bao','bla2','bao@example.com', '0773585487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('olivier','bla3','oliver@example.com', '0763485487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('mehdi','bla4','mehdi@example.com', '0663585487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('john','bla5','john@example.com', '0763785487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('alex','bla6','alex@example.com', '0789585487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('mufasa','bla7','mufasa@example.com', '0783585487'))
cur.execute("INSERT INTO Membres (login,password,mail, numero_tel) VALUES (?,?,?,?)",('lamar','bla8','lamar@example.com', '0963585487'))

cur.execute("INSERT INTO Velos (hauteur, longueur, statut) VALUES (?,?,?)",(50,100,'En reparation'))
cur.execute("INSERT INTO Velos (hauteur, longueur, statut) VALUES (?,?,?)",(60,120,'Indisponible'))
cur.execute("INSERT INTO Velos (hauteur, longueur, statut) VALUES (?,?,?)",(70,140,'Indisponible'))
cur.execute("INSERT INTO Velos (hauteur, longueur, statut) VALUES (?,?,?)",(50,100,'Disponible'))
cur.execute("INSERT INTO Velos (hauteur, longueur, statut) VALUES (?,?,?)",(60,120,'Disponible'))


cur.execute("INSERT INTO Reservations (id_membre,id_velo, code, date_deb,date_fin) VALUES (?,?,?,?,?)",(1,2, 4524,'2024-04-18','2024-04-19'))
cur.execute("INSERT INTO Reservations (id_membre,id_velo, code, date_deb,date_fin) VALUES (?,?,?,?,?)",(3,3, 5654, '2024-04-18','2024-04-19'))


cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(1,2,'2024-04-18','2024-04-19'))
cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(1,2,'2024-04-17','2024-04-18'))
cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(3,1,'2024-04-17','2024-04-18'))
cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(4,3,'2024-04-17','2024-04-18'))
cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(5,4,'2024-04-17','2024-04-18'))
cur.execute("INSERT INTO Historique (id_membre,id_velo,date_deb,date_fin) VALUES (?,?,?,?)",(6,5,'2024-04-17','2024-04-18'))

connection.commit()

# Close the connection
connection.close()
