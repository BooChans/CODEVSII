import sqlite3
import flask
from werkzeug.security import generate_password_hash, check_password_hash
from .exceptions import MembreExistedeja, Membrenexistepas


connection = sqlite3.connect('BDD_velos.db')

cur = connection.cursor()

def get_profil(login):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.row_factory = sqlite3.Row

    profil = cur.execute("SELECT * FROM Membres WHERE login=?", (login,)).fetchone()
    return profil

def ajouter_membre(login, mdp, mail):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.execute("SELECT login FROM Membres WHERE login=? OR mail = ?", (login,mail))
    existing_login = cur.fetchone()
    if existing_login:
        return MembreExistedeja(login,mail)
    else:
        mdp_hache = generate_password_hash(mdp)
        cur.execute("SELECT COUNT(id_membre) FROM Membres")
        c = cur.fetchone()
        cur.execute("INSERT INTO Membres (id_membre, login, password, mail) VALUES (?, ?, ?, ?)", ((c[0]+10000), login, mdp_hache, mail))
        connection.commit()
        print(f"Le membre avec l'identifiant {c[0]+1} a été ajouté avec succès.")
        connection.close()

def supprimer_membre(login, mdp, mail):
    cur.execute("DELETE FROM Membres WHERE login=? AND password=? AND mail=?", (login, mdp, mail))
    connection.commit()
    if cur.rowcount > 0:
        print("Membre supprimé avec succès.")
    else:
        print("Aucun membre correspondant trouvé.")

def changer_mdp(login, mdp, new_mdp):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.execute("SELECT password FROM Membres WHERE login=?", (login,))
    existing_password = cur.fetchone()
    if existing_password:
        if check_password_hash(existing_password[0], mdp):
            new_mdp_hash = generate_password_hash(new_mdp)
            cur.execute("UPDATE Membres SET password=? WHERE login=?", (new_mdp_hash, login))
            connection.commit()
            print("Mot de passe changé avec succès.")
        else:
            print("Mot de passe incorrect.")
    else:
        print("Aucun utilisateur correspondant trouvé.")

def affiche_profil(login):
    b,c= get_profil(login)
    print("vos informations : \n")
    print("login : ",b,  "\n") 
    print("mail : ",c," \n") 


connection.commit()
connection.close()

