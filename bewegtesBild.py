
import numpy as np
import matplotlib.pyplot as plt
import pylab

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()
fig = plt.figure()

for n in range(0,100,1):
	y = np.random.rand(10,1)
	plt.plot(y)
	plt.show()
	fig.canvas.draw()
	plt.clf()
	
	