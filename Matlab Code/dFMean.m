%% File to compute averaged Z scored dFF

%% Set Pathway
AnnFileB = A; 
%% Variables 1

X1=nan(length(AnnFileB),1);

for i = 1:length(AnnFileB)
    %% Load Data
    i
    matfile = regexprep(AnnFileB{i},'.txt','.mat');
    [Fstart, Fstop, behaviors] = inputtext(AnnFileB{i});
    load (matfile,'Lfilter', 'FL', 't'); 
    if size(Lfilter, 2) ==1
        Lfilter = Lfilter';
    end
    W = floor(length(Lfilter)/FL/10);
    Lflat = zeros(size(Lfilter));
    Lflat(ceil(10*FL):end) = msbackadj((ceil(10*FL)/FL:1/FL:length(Lfilter)/FL)', ...
        Lfilter(ceil(10*FL):end)', 'StepSize', W, 'windowsize', W,'SHOWPLOT',0);
    Lbackground = Lfilter-Lflat;
    Lfilter = Lflat./Lbackground;  %deltaF/F
  

    %% Get the raw trace Onset and Offset

    Lz = (Lfilter - mean(Lfilter))/std(Lfilter);
    intro_id = strfind_part(behaviors, {'Male'});
    removal_id = strfind_part(behaviors, {'Male'});
    
    [X1(i)] = mean(GCamP_mean_BD(Lz, t, FL, behaviors, Fstart, Fstop, {'Attack'}, intro_id(1), removal_id(end)));
    
   
end
