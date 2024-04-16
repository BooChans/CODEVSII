def MembreExistedeja(login, mail):
  raise Exception("Le membre " + login + " ou l'email " + mail + " existe déjà !")

def Membrenexistepas(login):
  raise Exception("Le membre " + login + "n'existe pas")

def Reservationdejaprise(login):
  raise Exception("L'utilisateur a déjà réservé un vélo pour la journée")

