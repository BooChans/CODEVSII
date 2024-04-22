import sqlite3
import flask

def ModifEtatMembre(id_membre, etat):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Membres SET etat = ? WHERE id_membre = ?", (etat, id_membre))
    connection.commit()
    connection.close()
    
def MakeAdmin(id_membre):
    ModifEtatMembre(id_membre, admin)

def RemoveAdmin(id_membre):
    ModifEtatMembre(id_membre, normal)

def ModifStatutVelo(id_velo, statut):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Velos SET statut = ? WHERE id_velo = ?", (statut, id_velo))
    connection.commit()
    connection.close()
