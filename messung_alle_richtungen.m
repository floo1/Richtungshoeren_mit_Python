% Skript fuehrt eine Richtungsmessung fuer n_richtungen durch und gibt dabei
% dem Benutzer Anweisungen, die Petra relativ zum Lautsprecher im Uhrzeigersinn
% zu drehen (0->360 Grad). Anschließend wird jedes Signal vom rechten und 
% linken Ohr gespeichert, sowie das wiedergegebene Ausgangsrauschen und als
% wave-Datei abgespeichert. 
% ----------------------------------------
% Parametererklaerung:      n_richtungen ................. Einstellungspositionen des Lautsprechers relativ zum Petra-Kunstkopf
%                           name_kk ...................... Name des Kunstkopfes
%                           petra_abspielen_aufnehmen .... naehre Infos siehe Skript 
%                           wk ........................... Winkelposition
% ---------------------------------------

%% Parameter 
n_richtungen = 8

delta_winkel = 360/n_richtungen;

name_kk = 'petra'


for wk = 1:n_richtungen,
    richtung = (wk-1)*delta_winkel;
    fprintf('bitte den Lautsprcher(!) auf %g Grad rel. zu vorne einstellen, gemessen gegen uhrzeigersinn\n', richtung);
    input ('OK?  (press RETURN)  ')
    
    petra_abspielen_aufnehmen;    
    
    fprintf('aufnahmen und wiedergabe werden in wavs gespeichert...\n')
    
    name_links = sprintf('hrir_links_%s_%dgrad', name_kk, richtung)
    name_rechts = sprintf('hrir_rechts_%s_%dgrad', name_kk, richtung)
    name_play = sprintf('hrir_wiedergabe_%s_%dgrad', name_kk, richtung)
    
    wavwrite(aufnahme(:,1),fs, 24,name_links);
    wavwrite(aufnahme(:,2),fs, 24,name_rechts);    
    wavwrite(wiedergabe, fs, 24,name_play);    
end
