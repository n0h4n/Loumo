#coding=UTF-8
import tkinter

global scrollbar

def Effacer(root):
	for widget in root.winfo_children():
			widget.destroy()

############################################ MENU PRINCIPAL ####################################################
def MenuPrincipal(root):
			Effacer(root)
			tkinter.Label(root,text="Loumo").grid(
													column=0,
													row=0
													)
			tkinter.Label(root,text="N°Serveur").grid(
												column=0,
												row=1,
												sticky=tkinter.W
												)
												
			tkinter.Entry(root,width=15,text=root.NumServeur,fg="blue",bg="white").grid(
																	column=1,
																	row=1,
																	sticky=tkinter.W
																	)
			
			tkinter.Label(root,text="Cléf d'accès").grid(
												column=0,
												row=2,
												sticky=tkinter.W
												)

			tkinter.Entry(root,width=15,text=root.Clef,fg="blue",bg="white").grid(
																	column=1,
																	row=2,
																	sticky=tkinter.W
																	)
			tkinter.Label(root,text="Salle").grid(
												column=0,
												row=3,
												sticky=tkinter.W
												)

			tkinter.Entry(root,width=15,text=root.Salle,fg="cyan",bg="white").grid(
																	column=1,
																	row=3,
																	sticky=tkinter.W
																	)

			tkinter.Checkbutton(root, text="Sauvegarder les informations", variable=root.sauvegarde_infos).grid(
												column=0,
												row=4,
												sticky=tkinter.E
												)
			tkinter.Button(root,text="Connexion",command=root.init_connexion).grid(
												column=1,
												row=4
												)
			tkinter.Button(root,text="Paramètres",command=lambda:MenuParametres(root)).grid(
												column=0,
												row=5
												)

############################################ MENU PARAMETRES ####################################################

def MenuParametres(root):
			Effacer(root)
			tkinter.Label(root,text="Paramètres").grid(
													column=0,
													row=0
													)
			tkinter.Button(root,text="Retour",command=lambda:MenuPrincipal(root)).grid(
												column=0,
												row=5
												)
########################################## MENU CONNEXION ######################################################

def MenuConnexion(root):
			Effacer(root)
			tkinter.Label(root,text="Loumo").grid(
													column=0,
													row=0
													)
			tkinter.Label(root,text="Status:  ").grid(
												column=0,
												row=1,
												sticky=tkinter.W
												)
			tkinter.Label(root,textvariable=root.Statut,fg="purple").grid(
												column=1,
												row=1,
												sticky=tkinter.W
												)
			tkinter.Button(root,text="Annuler",command=root.AnnulerConnexion).grid(
												column=0,
												row=3,
												sticky=tkinter.W
												)
##########################################      SALLE    ######################################################

def Salle(root):
	Effacer(root)
	tkinter.Label(root,text=root.Salle.get()).grid(
													column=0,
													row=0,
													sticky=tkinter.W
													)
	frame_list_client = tkinter.Frame(root,bg="black",width=10,height=30)
	frame_list_client.grid(column=2,
								row=1,
								sticky=tkinter.W+tkinter.N)
	tkinter.Label(root,text="[{}] {}".format(root.client.Grade,root.client.Pseudo),fg="#3BFF99",justify=tkinter.LEFT).grid(
													column=2,
													row=0,
													sticky=tkinter.W 
													)
	
	tkinter.Label(frame_list_client,fg='white',text="Liste des clients").grid(
																			column=0,
																			row=0)
	tkinter.Label(frame_list_client,fg='white',textvariable=root.ClientListe,bg="black",justify=tkinter.LEFT,font=('Fixedsys',5),).grid(
													column=0,
													row=1,
													sticky=tkinter.W+tkinter.N
													)
	root.DeployerChat()
	
	e = tkinter.Entry(root,width=15,text=root.chat_a_envoyer,fg="green",bg="white")
	e.grid(
																	column=0,
																	row=2,
																	sticky=tkinter.W+tkinter.E
																	)
	e.bind('<Return>',root.EnvoyerChat)
	tkinter.Button(root,text="Envoyer",command=root.EnvoyerChat).grid(column=0,
																		 row=3,
																		 sticky=tkinter.E
															  	  )
	tkinter.Button(root,text="Déconnexion",command=root.Quitter).grid(column=0,
																		 row=3,
																		 sticky=tkinter.W
															  	  )
	
