import sqlite3


connection = sqlite3.connect('BDD_velos.db')

cur = connection.cursor()

def get_profil(login):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.row_factory = sqlite3.Row

    profil = cur.execute("SELECT * FROM Membres WHERE login=?", (login)).fetchone()
    a,b,_,d = profil
    return a,b,d

def ajouter_membre(login, mdp, mail):
    connection = sqlite3.connect('BDD_velos.db')

    cur = connection.cursor()
    cur.execute("SELECT login FROM Membres WHERE login=?", (login))
    existing_login = cur.fetchone()
    if existing_login:
        print(f"Le login {login} existe déjà dans la table Membres.")
    else:
        cur.execute("SELECT COUNT(id_membre) FROM Membres")
        c = cur.fetchone()
        cur.execute("INSERT INTO Membres (id_membre, login, password, mail) VALUES (?, ?, ?, ?)", ((c+1), login, mdp, mail))
        connection.commit()
        print(f"Le membre avec l'identifiant {identifiant} a été ajouté avec succès.")
        connection.close()

def supprimer_membre(login, mdp, mail):
    cur.execute("DELETE FROM Membres WHERE login=? AND password=? AND mail=?", (login, mdp, mail))
    connection.commit()
    if cur.rowcount > 0:
        print("Membre supprimé avec succès.")
    else:
        print("Aucun membre correspondant trouvé.")

def changer_mdp(login, mdp, new_mdp):
    cur.execute("UPDATE Membres SET password=? WHERE login=? AND password=?", (new_mdp, login, mdp))
    connection.commit()
    if cur.rowcount > 0:
        print("Mot de passe changé avec succès.")
    else:
        print("Aucun utilisateur correspondant trouvé ou mot de passe incorrect.")

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


def affiche_profil(login):
    a,b,c= get_profil(login)
    print("vos informations : \n")
    print("identifiant : ",a, "\n")
    print("login : ",b,  "\n") 
    print("mail : ",c," \n")  

supprimer_membre("BaoChau TRAN",123,"baochau@mail.com")
connection.commit()
connection.close()

