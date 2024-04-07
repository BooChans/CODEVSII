<<<<<<< HEAD
def MembreExistedeja(login, mail):
  raise Exception("Le membre " + login + " ou l'email " + mail + " existe déjà !")

def Membrenexistepas(login):
  raise Exception("Le membre " + login + "n'existe pas")
=======
def MembreExistedeja(login):
  return Exception("le membre" + login + " existe déjà")

def Membrenexistepas(login):
  return Exception("le membre" + login + "n'existe pas")
>>>>>>> 4e16e73196785e29a0f74c2f753dd0937a9c72ba

