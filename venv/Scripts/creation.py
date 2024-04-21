import sqlite3

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

cur.execute("DROP TABLE IF EXISTS Historique")
cur.execute("DROP TABLE IF EXISTS Reservations")
cur.execute("DROP TABLE IF EXISTS Velos")
cur.execute("DROP TABLE IF EXISTS Membres")

cur.execute("""CREATE TABLE Membres(
    id_membre INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    mail TEXT UNIQUE NOT NULL,
    numero_tel TEXT UNIQUE NOT NULL
)""")

cur.execute("""CREATE TABLE Velos(
    id_velo INTEGER PRIMARY KEY AUTOINCREMENT,
    hauteur REAL NOT NULL,
    longueur REAL NOT NULL,
    statut TEXT NOT NULL
)""")

cur.execute("""CREATE TABLE Reservations(
    id_res INTEGER PRIMARY KEY AUTOINCREMENT,
    id_membre INTEGER,
    id_velo INTEGER,
    code INTEGER,
    date_deb DATETIME,
    date_fin DATETIME,
    FOREIGN KEY (id_velo) REFERENCES Velos(id_velo),
    FOREIGN KEY (id_membre) REFERENCES Membres(id_membre) 
)""")

cur.execute("""CREATE TABLE Historique(
    id_res INTEGER PRIMARY KEY,
    id_membre INTEGER,
    id_velo INTEGER,
    date_deb DATETIME,
    date_fin DATETIME,
    FOREIGN KEY(id_res) REFERENCES Reservations(id_res),
    FOREIGN KEY(id_velo) REFERENCES Velos(id_velo),
    FOREIGN KEY(id_membre) REFERENCES Membres(id_membre) 
)""")
