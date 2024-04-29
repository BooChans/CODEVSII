import sqlite3
import flask
import random
import datetime

connection = sqlite3.connect('BDD_velos.db')
cur = connection.cursor()

def get_historique_velo_client(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM Historiques WHERE id_velo = ?", (id_velo,))
    t = cur.fetchall()
    hist = []
    for res in t :
        hist.append(res)
    return hist

def get_historique_membre(login):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM Historiques JOIN Membres AS m ON m.id_membre = id_membre WHERE m.login = ?", (login,))
    t = cur.fetchall()
    hist = []
    for res in t :
        hist.append(res)
    return hist

def get_all_historique():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM Historiques")
    t = cur.fetchall()
    hist = []
    for res in t :
        hist.append(res)
    return hist

def get_historique(date_deb, date_fin):
    cur.execute("SELECT * FROM Historiques WHERE date_deb >= ? AND date_fin >= ?", (date_deb, date_fin))
    t = cur.fetchall()
    hist = []
    for res in t :
        hist.append(res)
    return hist

def effacer_historique_membre(login):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique AS h JOIN Membres AS m ON h.id_membre = m.id_membre WHERE login =?", (login,))
    connection.commit()

def effacer_historique_velo(id_velo):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique WHERE id_velo = ?", (id_velo,))
    connection.commit()

def effacer_historique():
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM Historique ")
    connection.commit()
    
