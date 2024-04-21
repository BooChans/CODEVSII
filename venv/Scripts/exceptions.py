def MembreExistedeja(login, mail,numero_tel):
  raise Exception("Le membre " + login + " ou l'email " + mail + " ou le numéro de téléphone " + numero_tel + " existe déjà !")

def Membrenexistepas(login):
  raise Exception("Le membre " + login + "n'existe pas")

def Reservationdejaprise(login):
  raise Exception("L'utilisateur a déjà réservé un vélo pour la journée")

def Dejareserve():
  raise Exception("Vélo déjà réservé")

