#coding=UTF-8

import socket
import threading
from auth import *
import time


SERV_MESSAGE = """Bienvenue sur le serveur InDev LOUMO
Le serveur est vraiment instable ce qui
peux entrainer de nombreux bugs et crashs
Attention; Il n'y a pas de couche de sécurité (TLS)
Donc les données transmises au serveur ne sont
pas cryptées et peuvent donc être interceptées
Evitez donc de transmettre des données sensible telle
que des mots de passe.

- Nohan
"""

class Serveur(socket.socket):
	def __init__(self,hote="192.168.0.22",port=10030):
		self.EnRoute = True
		self.Clients = dict()
		self.hote = hote
		self.port = port
		socket.socket.__init__(self,socket.AF_INET,socket.SOCK_STREAM)
		self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.Initialiser()
	
	def Initialiser(self):
		self.bind((self.hote,self.port))
		self.authentificateur = Authentificateur()
		self.EcouterConnexions()

	def EcouterConnexions(self):
		self.listen(2)
		print("En attente de connexions")
		while self.EnRoute:
			connexion, addr = self.accept()
			Client(self,connexion,addr)

class Client(threading.Thread):
	def __init__(self,root,connexion,addr):
		self.EnRoute = True
		self.Authentifie = False
		self.root = root
		threading.Thread.__init__(self,target=self.EcouterDonnees)
		self.connexion, self.addr = connexion, addr
		print("Nouvelle connexion ({})".format(self.addr))
		self.start()

	@staticmethod
	def EnvoyerTous(root,message):
		for client in root.Clients:
			root.Clients[client].EnvoyerDonnees(message)
	
	@staticmethod
	def Rafraichir_Tous(root):
		for client in root.Clients:
			root.Clients[client].Rafraichir_client_list_client()

	def Authentifier(self,clef):
		self.root.authentificateur.Authentifier(self,clef)
	
	def EcouterDonnees(self):
		while self.EnRoute:
			try:
				donnees = self.connexion.recv(1024)
				#print("DONNEES: {}".format(donnees.decode()))
			except:
				self.Eteindre()
			self.Traitement(donnees)
	
	def Traitement(self,donnees):
		print("Traitement des donnees")
		donnees = donnees.decode()
		donnees = donnees.split('#')
		for infos in donnees:
			infos = infos.split(':')
			print(infos)
			if(infos[0] == "CLEF"):
				print("CLEF RECU")
				self.clef = infos[1]
				self.Authentifier(self.clef)
			
			if(self.Authentifie):
				if(infos[0] == "STATUT"):
					if(infos[1] == "PRET"):
						self.Pret()
					if(infos[1] == "ENTREE"):
						Client.EnvoyerTous(self.root,"CHAT:[SERVEUR] [{}]{} à rejoint la salle".format(self.Grade,self.Pseudo))
				
				if(infos[0] == "CHAT"):
					Client.EnvoyerTous(self.root,"CHAT:<[{}]{}>{}".format(self.Grade,self.Pseudo,infos[1]))
		

	def Activer(self,grade,pseudo):
		self.Authentifie = True
		self.Pseudo = pseudo
		self.Grade = grade
		self.EnvoyerDonnees("STATUT:AUTHENTIFIE:{}:{}".format(self.Grade,self.Pseudo))
		self.EnvoyerDonnees("SERV_MESSAGE:{}".format(SERV_MESSAGE))
		
	def Pret(self):
		print("{} est prêt".format(self.Pseudo))
		self.root.Clients[self.clef] = self
		#self.Rafraichir_client_list_client()
		self.EnvoyerDonnees("STATUT:OK")
		Client.Rafraichir_Tous(self.root)

	def Rafraichir_client_list_client(self):
		liste = str()
		for client in self.root.Clients:
			liste += "!{},{}".format(self.root.Clients[client].Grade,self.root.Clients[client].Pseudo)
		self.EnvoyerDonnees("CLIENT_LIST:{}".format(liste))
	
	def Ejecter(self,raison):
		self.EnvoyerDonnees("STATUT:EJECTE:{}".format(raison))
		self.Eteindre()
	
	def Eteindre(self):
		self.EnRoute = False
		print("{} s'est déconnecté".format(self.addr))
		try:
			del self.root.Clients[self.clef]
			Client.EnvoyerTous(self.root,"CHAT:[SERVEUR] [{}]{} s'est déconnecté#".format(self.Grade,self.Pseudo))
		except:
			print("{} n'etait pas authentifié".format(self.addr))
		time.sleep(1)
		Client.Rafraichir_Tous(self.root)
	
	def EnvoyerDonnees(self,donnees):
		print("Envoie {}".format(donnees))
		#try:
		self.connexion.send(donnees.encode())
		#except Exception as ex:
		#	print("ERREUR:{}".format(ex.__class__.__name__))
		#	self.Eteindre()
Serveur()
