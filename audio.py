#coding=UTF-8

import pyaudio
import threading

CHUNK = 16
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44000

class Micro(pyaudio.PyAudio):
	def __init__(self,root):
		pyaudio.PyAudio.__init__(self)
		self.root = root
		self.Mute = False
		self.stream_mic = self.open(format=FORMAT,
							channels=CHANNELS,
									rate=RATE,
									input=True,
						frames_per_buffer=CHUNK)
		self.EnvoieFlux = threading.Thread(target=self.FluxLoop)
		
	def FluxLoop(self):
		self.root.info("Lancement d'un nouveau THREAD de flux audio")
		self.root.info("Envoie du flux de données")
		while not self.Mute:
			self.root.client.EnvoyerDonnees("{}".format(self.Lire()))
	
	def Lire(self):
		data = self.stream_mic.read(CHUNK)
		return data

class HautParleur(pyaudio.PyAudio):
	def __init__(self,root):
		self.root = root
		pyaudio.PyAudio.__init__(self)
		self.stream_hp = Micro.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
				output=True,
                frames_per_buffer=CHUNK,
				self=self)	

	def Ecrire(self,donnees):
		self.stream_hp.write(donnees)

