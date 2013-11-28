% Dieses Script spielt ein Breitbandrauschen ueber Lautsprecher ab und wird am Kunstkopf 
% Petra am linken und rechten Ohr durch eine Soundkarte aufgenommen. 
% ----------------------------
% Skript wird in messung_alle_richtungen.m ausgefuehrt 
% ----------------------------
% Parametererklaerung:  fs ............... Abtastfrequenz
%                       device_index ..... ermittelter Ein- und Ausgangsweg der
%                       TASCAM-Soundkarte durch msound('deviceInfo'), nicht
%                       Ausfuehrbar wenn Soundkarte nicht angeschlossen!!!
%                       time ............. Dauer des wiedergegebenenRauschen
%                       figure(1) ........ Plot zeigt zeitliche Aufnahme,
%                       Amplitude zwischen -1 und +1             
% ---------------------------

% Parameter
fs =44100;
block_len = 2*1024;%2048;   
device_index = [2 6]; %[2 4] sind fuer das internen Mikrofon und Lautsprecher
time = 2;

% Aufnahme des Rauschens mit Petra Kunstkopf
msound('openRW', device_index, fs, block_len, 2);

n_blocks = round(fs*time/block_len);

% vorher Platz vorbereiten
aufnahme = zeros(n_blocks*block_len,2);
wiedergabe = aufnahme(:,1);     

% 10 Rausch-Bloecke werden abgespielt ...
for k=1:10,
    not_used = msound('getsamples');
    noise_play = 0.05*randn(block_len,1);
    msound('putsamples',[noise_play noise_play]);
end

% ... bis weiteres Rauschen mit Aufnahme einsetzt
for k = 1:n_blocks
    noise_play = 0.05*randn(block_len,1);
    msound('putsamples',[noise_play noise_play]);
    wiedergabe((k-1)*block_len + (1:block_len),:) = noise_play;
    noise_record = msound('getsamples');
    aufnahme((k-1)*block_len + (1:block_len),:) = noise_record;  
end

msound('close')
%figure(1)
%plot(aufnahme)
