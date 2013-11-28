% Dieses Skript liest alle erstellten wave-Dateien ein und erstellt danach
% ein Dichteleistungsspektrum. Die DLS werden fuer jede Seite in einem Plot
% dargestellt
% -------------------------------------------
% Parametererklaerung: 
% -------------------------------------------

clear 

%% Parameter
name_kk = 'petra'
block_len = 1024
delta_winkel = 45;
n_richtungen = 360/delta_winkel;
winkel = (0:n_richtungen-1)*delta_winkel

for kk = 1:n_richtungen
    
    richtung = (kk-1)*delta_winkel,
    name_links = sprintf('hrir_links_%s_%dgrad', name_kk, richtung)
    name_rechts = sprintf('hrir_rechts_%s_%dgrad', name_kk, richtung)
    name_play = sprintf('hrir_wiedergabe_%s_%dgrad', name_kk, richtung)

    [links,fs] = wavread(name_links);
    rechts = wavread(name_rechts);
    wiedergabe = wavread(name_play);
    
    figure(kk)
    [pxxl, w] = pwelch(links, block_len);
    [pxxr, w] = pwelch(rechts, block_len);
    plot(w/pi*fs/2,[10*log10(pxxl) 10*log10(pxxr)] )
    title(sprintf('richtung %d', richtung))     

end

