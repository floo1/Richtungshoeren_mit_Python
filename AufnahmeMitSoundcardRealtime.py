###Script zum Real-time-plotting aufgenommender Datein als Array mit Mikrofonen,
###waehlbare Anzahl des Realtime-Plots 
###Autor: Andreas Minch, 06.11.13
###Originalsourcecodes: bastibe.de und github.com/bastibe/PySoundCard
###Version: V.03
###Benutzung:!!!Hier muss vorher der cd-Ordner gewechselt werden, das Module matplotlib importiert und der Befehl prozent pylab qt4 im
###CommandWindow ausfuehren werden,
###da sonst bei Windows Plotfenster im Command window erscheinen wuerden!!!

############# laden classes aus modules ##############
import sys
import matplotlib.pyplot as plt
import matplotlib
import pyaudio
import numpy as np
from pysoundcard import Stream
p = pyaudio.PyAudio() 

#################### vorheriges Fenster schliessen ###############
plt.close() #Fenster von der vorhergehenden Aufnahme schliessen

############# Aufnahmeparameter #############
fs = 44100
block_length = 64
record_seconds = 10
CHANNELS = 2
n_down_plot = 50 #Variable Anzahl Plotts pro Sekunde

############ Stream mit Zugriffswegen fuer externe Soundkarte ##########
s = Stream(sample_rate = fs, 
           block_length = block_length,
           input_device_index = 1, #im CommandWindow den Weg herausfinden mit import pyaudio, py=pyaudio.PyAudio(), pa.get_device_info_by_index(NUMMERVERSUCH)
           output_device_index = 4) 

fig, ax = plt.subplots()
s.start()
plt.show(block=False) #Plot wird im Fenster gelöscht und neu geschrieben

ca_whole_record = []
num_of_blocks = int(fs*record_seconds/block_length)
line, = ax.plot(np.random.randn(num_of_blocks)*15-50) #Skalierung der y-Achse
pegel = np.zeros(num_of_blocks) #Nullvektor erstellen als Ausgang

for n in range(num_of_blocks): #geht die Schleife solange durch, bis 
    ca_record = s.read(block_length)
    pegel[n] = 10*np.log10(np.sum(np.square(ca_record))/block_length) #Pegel auf logarithmischer y-Achse darstellen 
    ca_whole_record.append(ca_record) #haengt alle in blocklaenge aufgenommenes Array

    if np.mod(n, n_down_plot) == 0: #Modul-Befehl fuer Rest berechnen, damit nur soviel wie n_down_plot im Plotfenster gezeigenangezeigt wird
        line.set_ydata(pegel)
        ax.draw_artist(ax.patch)
        ax.draw_artist(line)
        fig.canvas.update()
        fig.canvas.flush_events()
s.stop()
print ("* done recording")
