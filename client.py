#coding=UTF-8

import socket
import threading
import time

class Client(socket.socket,threading.Thread):
	def __init__(self,root,cible,clef):
		self.EnRoute = True
		
		self.root, self.cible, self.clef = root, cible, clef
		self.root.info("Lancement du client")
		threading.Thread.__init__(self,target=self.EcouterDonnees)
		socket.socket.__init__(self,socket.AF_INET,socket.SOCK_STREAM)
		
		self.liste_client = dict()
		
		self.root.info("Connexion au serveur distant: ({})".format(cible))
		self.connecter()
		
		
	def connecter(self):
		for tentative in range(1,6):
			self.root.info("Connexion à la cible ({}/5)".format(tentative))
			try:
				self.connect(self.cible)
			except Exception as Ex:
				self.root.info("Echec",2)
				if(tentative == 5):
					if(not self.EnRoute):
						self.root.info("Annulation")
						return
					self.root.info("Connexion impossible CODE:{}".format(Ex.__class__.__name__))
					self.root.deiconify()
					self.root.Statut.set("Impossible de contacter le serveur")
					return
				else:
					continue
			break
		self.EnvoyerDonnees("CLEF:{}".format(self.clef))
		self.start() #lance le thread
		self.root.Statut.set("Connecté")
		self.root.info("Le client est prêt")

	
	def EcouterDonnees(self):
		self.root.info("Lancement d'un nouveau thread pour l'écoute des donnees")
		while self.EnRoute:
			message = self.recv(1024)
			self.Traitement(message)
	
	def Traitement(self,donnees):
		print("Traitement des donnees")
		donnees = donnees.decode()
		donnees = donnees.split('#')
		for infos in donnees:
			infos = infos.split(':')
			print(infos)
			if(infos[0] == "STATUT"):
				if(infos[1] == "AUTHENTIFIE"):
					self.root.info("Vous êtes authentifié !",1)
					self.Activer(infos[2],infos[3])
				if(infos[1] == "EJECTE"):
					self.Ejecter(infos[2])
				if(infos[1] == "OK"):
					self.root.RejoindreSalle()
			
			if(infos[0] == "SERV_MESSAGE"):
				self.root.SERV_MESSAGE.set(infos[1])
			
			if(infos[0] == "CLIENT_LIST"):
				donnees = infos[1].split('!')
				liste_str = str()
				print(donnees)
				for client in donnees:
					if(len(client) >1):
						info = client.split(',')
						liste_str+="[{}] {}\n".format(info[0],info[1])
				self.root.ClientListe.set(liste_str)
			
			if(infos[0] == "CHAT"):
				self.root.chat_list.insert('end', infos[1])


	
	def Activer(self,grade,pseudo):
		self.Grade = grade
		self.Pseudo = pseudo
		self.root.info("Identité: {},{}".format(self.Grade,self.Pseudo),1)
		self.root.Statut.set("Vous avez été Authentifié avec succès\nVotre identité est [{}] {}".format(self.Grade,self.Pseudo))
		self.root.Pret()
	
	def Ejecter(self,raison):
		self.root.info("Vous avez été éjecté du serveur ! ({})".format(raison),3)
		self.root.Statut.set("Vous avez été éjecté du serveur !\nRaison: {}".format(raison))
		self.EnRoute = False
		self.close()
	
	def Lancer(self):
		self.EnvoyerDonnees("STATUT:PRET")
	
	def EnvoyerDonnees(self,donnees):
		self.send(donnees.encode())
	
	def Detruire(self):
		self.EnRoute = False
		self.close()
