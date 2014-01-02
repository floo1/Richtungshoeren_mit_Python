# read HRTF levels of li and re
#
# such aus HRTF datei die Pegel von li und re für die jeweilige terz (bis 8kHz) heraus und schreibt die
# Pegeldifferenzen (in dB) in eine Matrix.
# speichern der Matrix in eine Text-Datai (eventuell für Matlab...) 
#
# S.Gibson


from numpy import *
import wave
from pysoundfile import SoundFile
from matplotlib.pyplot import *

#---------- testfile finden ----------------------------------------------------------------#
files = arange(0,90+5,5)

# matrix erzeugen
matrix = zeros(592).reshape((37, 16)) # Grad/Terzen
i = 18 # (also 19.zeile) für speicherung der Werte von 0-90 Grad, sollen im unteren Block stehen! damit ingesammt von -90 bis 90 

#----- jedes wavFile einzelnd lesen und pegeldifferenz bestimmen -------------------------------# 
for n in files:
	# mit %03 werden für 'n' die variablen 3-stelllig eingesetzt, wichtig am schluss %(n)!!
	pfadFile1 = '/Users/sam/python33/projekt/HRTF_KEMAR/elev10/H10e%03da.wav' %(n)
	readFile = wave.open(pfadFile1,'r')

	# ----------read fs from wavFile:-----------------------------------------------------------#
	fs = readFile.getframerate()


	# ----------read soundfile -----------------------------------------------------------------#
	soundfile = SoundFile(pfadFile1)[:] # als zeilenvektor: re und li ! 


	#------------Spektrum von signal -----------------------------------------------------------#
	signal = soundfile
	Nfft = len(signal)
	block_leng = len(signal)
	f_vec = (arange(block_leng)/block_leng)*fs   # f_vec enthält n-viele Frequenzen von 0 bis < Fs 
	f_vec = f_vec[0:int(block_leng/2)]              # f_vec von Fs auf Fs/2 teilen, wobei nicht sicher ob abrunden(n/2) oder aufrunden(n/2)
		
	fft_y = fft.fft(signal, axis = 0)/Nfft
	fft_y = fft_y[0:int(block_leng/2)] 
	fft_Ampl = abs(fft_y)
	fft_Pegel =20*log10(fft_Ampl)
	
	
	
	#------ Pegel aus Spektrum lesen / in Terzbändern---------------------------------------------#
	# erstmal für Mittenfrequenzen bis 8 kHz
	f_mid_vec = 250*2**arange(0,5.3,1/3) # 250,314,396,500,629,793,1000,1259,1587,2000,3174,4000,5039,6349,8000 Hz
	f_low = floor(f_mid_vec*2**(-2/12)/fs*Nfft)  # untere grenz-bin abrunden/ normieren auf FFT-Bins (daher=fs*Nfft)
	f_high = ceil(f_mid_vec*2**(2/12)/fs*Nfft) # oberer grenz-bin aufrunden
	
	pegel_li = zeros(len(f_mid_vec))  	 # speichert die maximalpegel jeder terz (li)
	pegel_li = pegel_li[:, newaxis]	# als spaltenvektor
	pegel_re = zeros(len(f_mid_vec))  	 # speichert die maximalpegel jeder terz (li)
	pegel_re = pegel_re[:, newaxis]	# als spaltenvektor
	
	for k in arange(0,16,1):
			k_low = f_low[k]
			k_high = f_high[k]
			# pegel links
			li_freq_pegel = fft_y[k_low:k_high+1,0] # bestimmte frequenz bins auswählen
			li_freq_pegel = 20*log10(abs(li_freq_pegel)) # aus diesem Spektrum die Pegel(dB) ermitteln
			#li_freq_pegel = abs(li_freq_pegel) # aus spektrum amplituden (rel) ermitteln
			li_max_pegel = max(abs(li_freq_pegel))*(-1) # maximalpegel dieser terz finden
			pegel_li[k] =  li_max_pegel	# in den vektor schreiben 
			
			# pegel rechts:
			re_freq_pegel = fft_y[k_low:k_high+1,1] # bestimmte frequenz bins auswählen
			re_freq_pegel = 20*log10(abs(re_freq_pegel)) # aus diesem Spektrum die Pegel(dB) ermitteln
			re_max_pegel = max(abs(re_freq_pegel))*(-1) # maximalpegel dieser terz finden
			pegel_re[k] =  re_max_pegel	# in den vektor schreiben 
	
	
	
	#---------- Pegeldifferenz bestimmen-------------------------------------#
	
	pegelDiff = abs(pegel_li - pegel_re).T 	#(.T = transponieren!)
	#pegelDiff = ones(16)+i 	#zum testen
	
	# speichern in matrix
	matrix[i,:] = pegelDiff #ablegen in i.te zeile
	i=i+1					# nächste Zeile


	
# jetzt stehen alle pegeldifferenzen von 0 bis 90 Grad in der Matrix.Für 0 bis -90 Grad vorhandene Werte invers verwenden, da Kopf ideal Rund!
# also alle werte von 0-90 Grad = * -1
neg = matrix[19:37,:]*(-1) # ergibt matrix von -5 bis -90 Grad,
# muss jetzt noch umgedreht werden zu -90 bis -5 Grad
pos1 = arange(0,18,1)
g = 17
for v in pos1:
	matrix[g,:] = neg[v,:]
	g=g-1

	
#-------- matrix als Textdatei speichern----------------------------------#

savetxt('Pegeldiff_matrix.txt', matrix, fmt='%2f', delimiter=', ', newline='\n', header='x = Terzen (0.-15.), y = Gradeinheiten (-90-+90Grad)')





'''
# Plot Eingangsspektrum von signal
subplot(221)
title('Spektrum Einganssignal')
plot(f_vec, fft_Pegel)
xlabel('Freq in Hz')
ylabel('Pegel in dB')
xlim(xmax=8000)

subplot(222)
plot(f_vec, fft_Ampl)
xlabel('Freq in Hz')
ylabel('Amplitude')
xlim(xmax=8000)

# plot maxPegel  
subplot(223)
plot(pegel_li)
plot(pegel_re)
x_vec = linspace(0,15,len(pegel_li))
#plt.bar(x_vec,pegel_li)
xlabel('Terzen')
ylabel('Pegel in dB')

#---plot pegeldifferenz--------------------#
subplot(224)
plot(pegelDiff)
xlabel('Terzen')
ylabel('Pegel in dB')

show()
'''