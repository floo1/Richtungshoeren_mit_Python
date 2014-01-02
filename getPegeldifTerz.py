from numpy import *
import matplotlib.pyplot as plt
from scipy.io.wavfile import *
from gen_sin import *

def getPegeldifTerz(signal,fs):

    Nfft = len(signal)
    
    #--------- Spektrum von Signal--------#

    # WICHTIG:  axis = 0 muss dabei stehen!!
    spec=np.fft.fft(signal, axis = 0)/Nfft    # spektrum von signal 
    spec_li = spec[:,0]    # aufteilen in rechtes und linkes spektrum 
    spec_re = spec[:,1]

    #----- Leistung der einzelen Bänder berechnen--#

    # die mittenfrequenzen sind definiert mit:
    f_mid_vec = 250*2**arange(0,5.3,1/3) # 250,314,396,500,629,793,1000,1259,1587,2000,3174,4000,5039,6349,8000 Hz
    f_low = ceil(f_mid_vec*2**(-2/12)/fs*Nfft)  # untere grenz-bin abrunden/ normieren auf FFT-Bins (daher=fs*Nfft)
    f_high = floor(f_mid_vec*2**(2/12)/fs*Nfft) # oberer grenz-bin aufrunden

    # einzelne terzleistung fuer jede Seite und jedes band
    powerVecSignal_li = zeros(len(f_mid_vec))
    powerVecSignal_li = powerVecSignal_li[:, np.newaxis]
    powerVecSignal_re = zeros(len(f_mid_vec))
    powerVecSignal_re = powerVecSignal_re[:, np.newaxis]

    # schleife berechnet in jeder terz die leistung
    for k in arange(0,16,1):
            k_low = f_low[k]
            k_high = f_high[k]
            #spektrale leistung nur von terzband berechnen
            band_li = spec_li[k_low+1:k_high] # nur ein terzband nehmen
            band_re = spec_re[k_low+1:k_high]
            # faktor 2, dabei leistung aus negativen freqn. mit beruecksichtigt wird.
            power_band_li = 2*sum(abs(band_li)**2) # betragsquadrat des fft-koeffizienten
            power_band_re = 2*sum(abs(band_re)**2)
            powerVecSignal_li[k] =  power_band_li
            powerVecSignal_re[k] =  power_band_re


    #--------hoechste Pegeldifferenzen finden-----#

    all_level_dif = 10*log10(powerVecSignal_re / powerVecSignal_li) # berechnet Pegeldifferenz in dB 
    find_idx = argmax(abs(powerVecSignal_li))             # findet idx von hoechsten wert von vektor (abs)=nur fuer mittenfrequenz
    mittenfrequenz = f_mid_vec[find_idx]    # such die mittenfrequenz abhaenging von idx
    terz_level_dif = all_level_dif[find_idx]                # sucht nur die terz mit hoechster leistung fuer rueckgabewert  

    # anzeigen in der schell
    #print('idx:',find_idx)
    #print('mittenfrequenz:',mittenfrequenz)
    #print('Pegeldifferenz (in dB):', terz_level_dif)
    
    return(terz_level_dif,mittenfrequenz, powerVecSignal_li, powerVecSignal_re)