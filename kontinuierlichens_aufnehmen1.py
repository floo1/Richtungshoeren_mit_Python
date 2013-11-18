# Rauschen abspielen und kontinuierlich in Blöcken aufnehmen

from pysoundcard import Stream
import pysoundcard
import numpy as np

fs = 44100
block_length = 8192
s = Stream(sample_rate=fs, block_length=block_length)
time = 3 # Laenge des Rauschens in Sekunden
noise = np.random.randn(block_length,2)/20.0 
n_blocks = int(fs*time/block_length)

# für das erste hinzufügen des ersten arrays einen start arry
# in passender größe, hier erstmal Nullen
rec_file=np.zeros([block_length,2],float) 

s.start()
for n in range(n_blocks):
	s.write(noise)
	rec = s.read(block_length)
	rec_file=np.vstack([rec_file,rec]) # hinzufügen des aufgenommenen blocks zu rec_file als zeilenvektor in einem array!
	
s.write(rec_file)
print(rec_file)
s.stop()