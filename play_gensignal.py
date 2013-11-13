# Signal erzeugen und abspielen

import sys
import numpy as np
import matplotlib as plt
from scipy.io.wavfile import read as wavread
from pysoundcard import Stream
  
block_length = 1024
fs =44100
time = 3
sample = time*fs

data = np.random.uniform(-0.7,0.7,sample)

s = Stream(fs, block_length)
s.start()
s.write(data)
s.stop()

