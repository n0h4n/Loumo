#coding=UTF-8

import socket
import ssl
import threading

CERTFILE = "Nohan.pem"

class Serveur(socket.socket):
	serveurs = []
	def __init__(self,hote="192.168.0.22",port=60600):
		self.EnRoute = True
		self.hote = hote
		self.port = port
		socket.socket.__init__(self,socket.AF_INET,socket.SOCK_STREAM)
		self.Initialiser()
	
	def Initialiser(self):
		self.wrappedSocket = ssl.wrap_socket(self,
											ca_certs="server.crt",
											cert_reqs=ssl.CERT_REQUIRED) server_side=True)
		self.wrappedSocket.bind((self.hote,self.port))
		self.EcouterConnexions()
	
	def EcouterConnexions(self):
		self.wrappedSocket.listen(2)
		print("En attente de connexions")
		while self.EnRoute:
			connexion, addr = self.wrappedSocket.accept()
			Client(connexion,addr)

class Client(threading.Thread):
	def __init__(self,connexion,addr):
		self.EnRoute = True
		threading.Thread.__init__(self,target=self.EcouterDonnees)
		self.connexion, self.addr = connexion, addr
		self.start()
	
	def EcouterDonnees(self):
		while self.EnRoute:
			donnees = self.connexion.recv(1024)
			print(donnees.decode())
	
	def EnvoyerDonnees(self,donnees):
		self.connexion.send(donnees)
		
Serveur()
