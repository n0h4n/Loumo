
import pyaudio
import wave
import threading


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "output.wav"

Micro = pyaudio.PyAudio()

stream_mic = Micro.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)


HP = pyaudio.PyAudio()
stream_hp = Micro.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)


print("Enregistrement")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	data = stream_mic.read(CHUNK)
	stream_hp.write(data)
	frames.append(data)





print("Lecture")
liste = list()
for frame in frames:
	stream_hp.write(frame)
	for item in frame:
		liste.append(item)

print(len(liste),type(frames))
print(liste)

stream_mic.stop_stream()
stream_mic.close()
Micro.terminate()


class Menu():
	def __init__(self,items):
		self.items = items
	
	def pack(self):
		for item in self.items:
			item.getWidget().grid(column=item.getPos(0),row=item.getPos(1),columnspan=item.getSpan(0),rowspan=item.getSpan(1))

	

class Item():
	def __init__(self,widget,grid_pos,grid_span):
		self.widget, self.grid_pos, self.grid_span = item, grid_pos, grid_span
	
	def getWidget(self):
		return widget
	
	def getPos(self,axe):
		if(axe == 0):
			return self.grid_pos[0]
		elif(axe == 1):
			return self.grid_pos[1]
	
	def getSpan(self,axe):
		if(axe == 0):
			return self.grid_span[0]
		elif(axe == 1):
			return self.grid_span[1]
