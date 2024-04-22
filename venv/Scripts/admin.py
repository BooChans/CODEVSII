import sqlite3
import flask

def ModifEtatMembre(id_membre, etat):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
<<<<<<< HEAD
    cur.execute("UPDATE Membres SET is_admin = ? WHERE id_membre = ?", (etat, id_membre))
=======
    cur.execute("UPDATE Membres SET etat = ? WHERE id_membre = ?", (etat, id_membre))
>>>>>>> 50746f1c5be8691fafbe7339551b1ae0d02747af
    connection.commit()
    connection.close()
    
def MakeAdmin(id_membre):
<<<<<<< HEAD
    ModifEtatMembre(id_membre, True)

def RemoveAdmin(id_membre):
    ModifEtatMembre(id_membre, False)
=======
    ModifEtatMembre(id_membre, admin)

def RemoveAdmin(id_membre):
    ModifEtatMembre(id_membre, normal)
>>>>>>> 50746f1c5be8691fafbe7339551b1ae0d02747af

def ModifStatutVelo(id_velo, statut):
    connection = sqlite3.connect('BDD_velos.db')
    cur = connection.cursor()
    cur.execute("UPDATE Velos SET statut = ? WHERE id_velo = ?", (statut, id_velo))
    connection.commit()
    connection.close()
