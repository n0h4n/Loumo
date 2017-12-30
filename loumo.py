#coding=UTF-8
import tkinter
import os
import struct

import menu
from client import *


SERVEUR_ADDR = "127.0.0.1"
SERVEUR_PORT = "60600"
VERSION = 0

class Application(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self.title("Loumo (Nohan)") #Titre
		self.option_add("*Font", "Fixedsys 10")
		self.geometry("600x600") #Taille fenetre
		self.resizable(width=False,height=False) #Ne pas rendre la taille de la fenetre modifiable
		self.protocol("WM_DELETE_WINDOW", self.Quitter)
		self.Initialiser()
		menu.MenuPrincipal(self)
		self.mainloop() #Lancement

	def Initialiser(self):
		self.tk_setPalette(background='#DCDCDC ')#, foreground='green',activeBackground='black', activeForeground='grey')
		
		self.NumServeur = tkinter.StringVar()
		self.Clef = tkinter.StringVar()
		self.Salle = tkinter.StringVar()
		self.sauvegarde_infos = tkinter.IntVar()
		
		self.SERV_MESSAGE = tkinter.StringVar()
		self.SERV_MESSAGE.set(" ERREUR: AUCUN MESSAGE ")
		
		self.ClientListe = tkinter.StringVar()
		
		self.Statut = tkinter.StringVar()
		self.Statut.set("Connexion en cours ...")
		
		self.chat_a_envoyer = tkinter.StringVar()
		
		self.info("Recherche du fichier de config")
		self.fichier = open("loumo.save","r")
		self.DejaEnregistres = self.fichier.readline()
		if(self.DejaEnregistres.replace("\n","") == "1"):
			self.info("Lecture du fichier config")
			self.NumServeur.set(self.fichier.readline().replace("\n",""))
			self.Clef.set(self.fichier.readline().replace("\n",""))
			self.Salle.set(self.fichier.readline().replace("\n",""))
			self.sauvegarde_infos.set(1)
		self.fichier.close()
		
		
	def init_connexion(self):
		self.info("Initialisation de la connexion")
		if(self.sauvegarde_infos.get() == 1):
			self.Sauvegarder()
		menu.MenuConnexion(self)
		threading.Thread(target=self.Connexion).start()
		
	def Connexion(self):
		self.info("Préparation")
		self.adresse = self.DecoderNumero(self.NumServeur.get())
		self.client = Client(self, (self.adresse,int(self.Salle.get()) )  ,self.Clef.get())
	
	def AnnulerConnexion(self):
		self.client.Detruire()
		menu.MenuPrincipal(self)
	
	def DecoderNumero(self,Numero):
		self.info(Numero)
		return socket.inet_ntoa(struct.pack('!L', int(Numero)))
	
	def Pret(self):
		tkinter.Button(self,text="Rejoindre la salle",command=self.client.Lancer).grid(column=1,
																			row=3,
																			columnspan=2)
		tkinter.Label(self,text="Message du serveur").grid(column=1,
															row=4,
															sticky=tkinter.W)
		tkinter.Label(self,textvariable=self.SERV_MESSAGE,justify=tkinter.LEFT,fg="grey").grid(column=1,
															row=5,
															sticky=tkinter.W)		
	
	def DeployerChat(self):
		self.scrollbar = tkinter.Scrollbar(self)
		self.chat_list = tkinter.Listbox(self,
										fg="green",
										highlightcolor="black",
										selectbackground="black",
										selectforeground="green",
										activestyle=None,
										highlightbackground="black",
										font=('Fixedsys',1),
										bg="black",
										width=45,height=30,
										yscrollcommand = self.scrollbar.set)
										 
		self.scrollbar.config( command = self.chat_list.yview )
		self.chat_list.grid(column=0,row=1)
		self.scrollbar.grid(column=1,
								row=1,
								sticky=tkinter.W+tkinter.N+tkinter.S)
	
	def EnvoyerChat(self,event=None):
		if(self.chat_a_envoyer.get() != ""):
			self.client.EnvoyerDonnees("CHAT:{}".format(self.chat_a_envoyer.get()))
			self.chat_a_envoyer.set("")
	
	def RejoindreSalle(self):
		self.info("Entrée dans la salle en cours")
		menu.Salle(self)
		self.client.EnvoyerDonnees("STATUT:ENTREE")
		self.info("Tout semble bon !")

	
	def Sauvegarder(self):
		self.info("Sauvegarde")
		os.remove("loumo.save")
		self.fichier = open("loumo.save","w+")
		self.fichier.write("1\n")
		self.fichier.write(self.NumServeur.get()+"\n")
		self.fichier.write(self.Clef.get()+"\n")
		self.fichier.write(self.Salle.get())
		self.fichier.close()
	
	def info(self,message,type=0):
		if(type == 0):
			self.type_msg = "INFO"
		elif(type == 1):
			self.type_msg = "ATTENTION"
		elif(type == 2):
			self.type_msg = "ERREUR"
		elif(type == 3):
			self.type_msg = "ERREUR FATALE"
		else:
			return
		
		message = "{} [{}] {} ".format(time.strftime("%H:%M:%S"),self.type_msg,message)
		print(message)
	
	def Quitter(self):
		self.fichier.close()
		self.destroy()
		self.client.Detruire()



Application()

input("Terminée\nAppuyez sur une touche pour continuer")

#Encoder une ip
#ip = IP
#packedIP = socket.inet_aton(ip)
#struct.unpack("!L", packedIP)[0]


