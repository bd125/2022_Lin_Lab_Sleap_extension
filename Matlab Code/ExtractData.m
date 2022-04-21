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
    matfile = regexprep(AnnFileB,'.txt','.mat');
    [~, ~, behaviors] = inputtext(AnnFileB);
    if ~isequal(exist(matfile, 'file'), 2)
        figure(1)
        TT = actxcontrol('TTank.X');
        invoke(TT, 'ConnectServer', 'Local','MyClient')
        invoke(TT, 'OpenTank', Tank, 'R')
        invoke(TT,'SelectBlock',Block)
        invoke(TT,'CreateEpocIndexing')
        N = TT.ReadEventsV(10000000, 'LMag', 0, 0, 0, 0, 'NODATA');
        num_channels = max(TT.ParseEvInfoV(0, N, 4));
        if num_channels >=3
            data = TDT2mat(Tank, Block, 'STORE', 'LMag', 'CHANNEL', 3);
            LMag = data.streams.LMag.data;
            FL = data.streams.LMag.fs;
         end
        if num_channels >=6
            data = TDT2mat(Tank, Block, 'STORE', 'LMag', 'CHANNEL', 6);
            LMag2 = data.streams.LMag.data;
            FL = data.streams.LMag.fs;
        else
            LMag2 = []; 
        end

        TT.CloseTank
        TT.ReleaseServer
        
        % get the time stamps of the video
        sr = seqIo(seqNm, 'reader');
        info=seqIo(seqNm,'getinfo'); n = info.numFrames;
        t = sr.getts(); t= t-t(1);
        [b, a] = butter(4, 3/FL, 'low');
        Lfilter = filtfilt(b, a, double(LMag));
        Lfilter2 = filtfilt(b, a, double(LMag2));loc =[];
        save(matfile, 'LMag','FL','LMag2', 'Lfilter', 'Lfilter2', 't', 'info', 'n', 'Tank', 'Block', 'seqNm', 'AnnFileB');
    end
end