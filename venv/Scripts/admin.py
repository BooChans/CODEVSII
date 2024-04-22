import sqlite3
import flask

def ModifEtatMembre(id_membre, etat):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Membres SET etat = ? WHERE id_membre = ?", (etat, id_membre))
    connection.commit()
    connection.close()
