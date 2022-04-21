% This script is used to extract the data from TDT Tank and to align the
% data with the videos and annotations. 

clc;clear
A = {};
%%
% path of the TDT data tanks
tS = {A{:,1}}';
% path of the TDT data blocks
bS = {A{:,2}}';
% path of the seq videos
sS = {A{:,3}}';
% path of the annotation files
aS = {A{:,4}}';

for i = 1:length(aS)
    Tank = tS{i};
    Block = bS{i};
    seqNm = sS{i};
    AnnFileB = aS{i};
    pathway = [Tank '\' Block];
    
    matfile = regexprep(AnnFileB,'.txt','.mat');
    [~, ~, behaviors] = inputtext(AnnFileB);
    if ~isequal(exist(matfile, 'file'), 2) %& ~isequal(exist(FPFile, 'file'), 2)
        
        % Extract data from Channel 3
        Data = TDTbin2mat(pathway,'STORE', 'LMag', 'CHANNEL', 3);
        LMag = Data.streams.LMag.data;
        FL = Data.streams.LMag.fs;

        % Extract data from Channel 6
        Data = TDTbin2mat(pathway,'STORE', 'LMag', 'CHANNEL', 6);
        LMag2 = Data.streams.LMag.data;
        FL = Data.streams.LMag.fs;
                 
        time = (1:length(LMag))/ FL;
        
        % get the time stamps of the video
        sr = seqIo(seqNm, 'reader');
        info=seqIo(seqNm,'getinfo'); n = info.numFrames;
        t = sr.getts(); t= t-t(1);
        [b, a] = butter(4, 3/FL, 'low');
        Lfilter = filtfilt(b, a, double(LMag));
        Lfilter2 = filtfilt(b, a, double(LMag2));loc =[];
        save(matfile, 'LMag','FL','LMag2', 'Lfilter', 'Lfilter2', 't', 'info', 'n','time', 'Tank', 'Block','seqNm');
    end
end
