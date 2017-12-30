#coding=UTF-8

CHEMIN_FICHIER = "users"


class Authentificateur():
	def __init__(self):
		print("Lancement de l'authentificateur")
		print("Lecture du fichier")
		self.fichier = open(CHEMIN_FICHIER,"r")
		self.accounts = dict()
		self.Actualiser()
	
	def Actualiser(self):
		while True:
			donnees = self.fichier.readline()
			if(donnees != ""):
				donnees = donnees.replace('\n','')
				donnees = donnees.split(' ')
				self.accounts[donnees[0]] = [donnees[1],donnees[2]]
			else:
				print(self.accounts)
				break
	
	def Authentifier(self,client,clef):
		if(clef in self.accounts):
			print("{} s'est authentifié avec succès -> ([{}] {})".format(client.addr,self.accounts[clef][0],self.accounts[clef][1]))
			client.Activer(self.accounts[clef][0],self.accounts[clef][1])
		else:
			print("Echec d'authentification de {}".format(client.addr))
			client.Ejecter("CLEF INVALIDE")
