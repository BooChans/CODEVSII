import sqlite3
import flask
<<<<<<< HEAD
from werkzeug.security import generate_password_hash, check_password_hash
from .exceptions import MembreExistedeja, Membrenexistepas
=======
>>>>>>> 4e16e73196785e29a0f74c2f753dd0937a9c72ba


connection = sqlite3.connect('BDD_velos.db')

cur = connection.cursor()

def get_profil(login):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.row_factory = sqlite3.Row

    profil = cur.execute("SELECT * FROM Membres WHERE login=?", (login)).fetchone()
    _,a,_,b = profil
    return a,b

def ajouter_membre(login, mdp, mail):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
<<<<<<< HEAD
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
=======
    cur.execute("SELECT login FROM Membres WHERE login=?", (login))
    existing_login = cur.fetchone()
    if existing_login:
        print(f"Le login {login} existe déjà dans la table Membres.")
    else:
        cur.execute("SELECT mail FROM Membres WHERE login=?", (mail))
        existing_mail = cur.fetchone()
        if existing_mail:
            print(f"Le mail {mail} existe déjà dans la table Membres.")
        else:
            mdp_hache = flask.generate_password_hash(mdp).encode('utf-8')
            cur.execute("SELECT COUNT(id_membre) FROM Membres")
            c = cur.fetchone()
            cur.execute("INSERT INTO Membres (id_membre, login, password, mail) VALUES (?, ?, ?, ?)", ((c+1), login, mdp_hache, mail))
            connection.commit()
            print(f"Le membre avec l'identifiant {c+1} a été ajouté avec succès.")
            connection.close()
>>>>>>> 4e16e73196785e29a0f74c2f753dd0937a9c72ba

def supprimer_membre(login, mdp, mail):
    cur.execute("DELETE FROM Membres WHERE login=? AND password=? AND mail=?", (login, mdp, mail))
    connection.commit()
    if cur.rowcount > 0:
        print("Membre supprimé avec succès.")
    else:
        print("Aucun membre correspondant trouvé.")

def changer_mdp(login, mdp, new_mdp):
    cur.execute("SELECT password FROM Membres WHERE login=?", (login,))
    existing_password = cur.fetchone()
    if existing_password:
        if check_password_hash(existing_password[0], mdp):
<<<<<<< HEAD
            new_mdp_hash = str(generate_password_hash(new_mdp),'utf-8')
=======
            new_mdp_hash = generate_password_hash(new_mdp).decode('utf-8')
>>>>>>> 4e16e73196785e29a0f74c2f753dd0937a9c72ba
            cur.execute("UPDATE Membres SET password=? WHERE login=? AND password=?", (new_mdp_hash, login, mdp))
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
<<<<<<< HEAD
    print("mail : ",c," \n") 

=======
    print("mail : ",c," \n")  
>>>>>>> 4e16e73196785e29a0f74c2f753dd0937a9c72ba

connection.commit()
connection.close()

