# Skript zur Darstellung der spektralen Phasendifferenz & Pegeldifferenz,
# zweier Kanäle eines Stereo_Vektors
# Autor: Franz Wichert, 10.11.13



from numpy import *
from pylab import *
from scipy import *


# Pegelschwelle definieren, durch die das Grundrauschen ignoriert werden soll
pegelschwelle = -100

# Erstellen des Testsignalvektors "stereo_vec"
#######################################
fs = 44100
dur = 1
t = arange(0,dur,1/fs)
	### Stereovektor mit Pegel-/Phasenunterschiedlicher Sinus ###
'''
f = 5000
sig_li = sin(2*pi*f*t)
sig_re = 2*sin(2*pi*f*t+pi/2)
'''
	### Stereovektor mit gleichen um 1 Sample verschobenes Rauschen auf beiden Kanälen ###

sig_main = np.random.randn(len(t))
sig_li = sig_main

n_delay = 6
sig_re = np.append(sig_main[n_delay:(len(sig_main))],sig_main[0:n_delay])
#sig_re = sig_re[0:len(sig_li)]


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

fft_y = (1/(fs*dur))*np.fft.fft(stereo_vec, axis = 0)	#(1/(fs*dur)) entspricht 1/N bei Fouriertransformation; => Python macht FFT ohne Faktor 1/N
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

# Alle fft-Werte, die als Pegel weniger als -100 dB ergeben werden auf 1 gesetzt
fft_y_li = [1 if 20*log10(abs(i)) < pegelschwelle else i for i in fft_y[:,0]]
fft_y_re = [1 if 20*log10(abs(i)) < pegelschwelle else i for i in fft_y[:,1]]


for m in range(0,len(fft_y),1):
	# Winkel berechnen
	li_Winkel[m,0] = angle(fft_y_li[m])
	re_Winkel[m,0] = angle(fft_y_re[m])
	# Pegel berechnen
	li_Pegel[m,0] = 20*log10(abs(fft_y_li[m]))
	re_Pegel[m,0] = 20*log10(abs(fft_y_re[m]))
	
	
# Winkeldiff berechnen	
Diff_Winkel = li_Winkel - re_Winkel
Diff_Winkel = np.unwrap(Diff_Winkel, discont = np.pi, axis = 0)		#unwrap verhindert Phasensprünge die über 2pi hinausgehen
# Pegeldiff berechnen
Diff_Pegel = li_Pegel - re_Pegel

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