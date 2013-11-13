# Skript zur Darstellung der spektralen Phasendifferenz & Pegeldifferenz,
# zweier Kanäle eines Stereo_Vektors
# Autor: Franz Wichert, 10.11.13



from numpy import *
from pylab import *
from scipy import *


# Erstellen des Testsignalvektors "stereo_vec"
#######################################
fs = 44100
dur = 1
t = arange(0,dur,1/fs)
f = 500
sig_li = sin(2*pi*f*t)
sig_re = 2*sin(2*pi*f*t+pi/2)

stereo_vec = zeros((len(sig_li),2))
stereo_vec[:,0] = sig_li
stereo_vec[:,1] = sig_re
########################################

#Erstellen der fft und Spektrums von "stereo_vec"
########################################
Fs = 44100
####
block_leng = len(stereo_vec)
f_vec = (arange(block_leng)/block_leng)*Fs	# f_vec enthält n-viele Frequenzen von 0 bis < Fs 
f_vec = f_vec[0:int(block_leng/2)] 			# f_vec von Fs auf Fs/2 teilen, wobei nicht sicher ob abrunden(n/2) oder aufrunden(n/2)

fft_y = np.fft.fft(stereo_vec, axis = 0)
fft_y = fft_y[0:int(block_leng/2)] 
fft_Pegel = 20*log10(abs(fft_y))
#######################################

#Plotten des Zeitverlaufs und Spektrums von "stereo_vec"
#######################################
plt.figure(1)

#Zeitverlauf	
plt.subplot(221)
plot(t,stereo_vec)
xlabel('t in [s]')
ylabel('Amplitude in [ ]')

#Spektrum
plt.subplot(222)
plot(f_vec, fft_Pegel)
xlabel('Freq in Hz')
ylabel('Pegel in dB')

#######################################

#Differenzen berechnen
#######################################

# Winkelvektoren erstellen
li_Winkel = np.zeros((len(fft_y),1))
re_Winkel = np.zeros((len(fft_y),1))

# Pegelvektoren erstellen
li_Pegel = np.zeros((len(fft_y),1))
re_Pegel = np.zeros((len(fft_y),1))


for m in range(0,len(fft_y),1):
	# Winkel berechnen
	li_Winkel[m,0] = math.atan(fft_y[m,0].imag/fft_y[m,0].real)
	re_Winkel[m,0] = math.atan(fft_y[m,1].imag/fft_y[m,1].real)
	# Pegel berechnen
	li_Pegel[m,0] = fft_Pegel[m,0]
	re_Pegel[m,0] = fft_Pegel[m,1]
	
	
# Winkeldiff berechnen	
Diff_Winkel = abs(li_Winkel - re_Winkel)
# Pegeldiff berechnen
Diff_Pegel = abs(li_Pegel - re_Pegel)

#########################################

#Plotten der spektralen Winkel- & Pegeldifferenzen
#########################################

plt.subplot(223)
plot(f_vec, Diff_Pegel)
xlabel('Freq in Hz')
ylabel('Pegeldiff in dB')

plt.subplot(224)
plot(f_vec, Diff_Winkel)
xlabel('Freq in Hz')
ylabel('Winkeldiff in rad')
show()