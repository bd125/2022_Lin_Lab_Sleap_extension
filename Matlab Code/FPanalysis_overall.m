%%
clc;clear
% Put all the annotation files in A
A = {};
%%

% i is corresponding to different mouse
for i =2
%% load DATA
AnnFileB = A{i};


matfile = regexprep(AnnFileB,'.txt','.mat');
[Fstart, Fstop, behaviors] = inputtext(AnnFileB);
load (matfile,'LMag','LMag2','Lfilter','Lfilter2','FL', 't'); 

%% Correct the baseline and calculate the dF/F 

% Lfilter
if size(Lfilter, 2) ==1
    Lfilter = Lfilter';
end
W = floor(length(Lfilter)/FL/10);
Lflat = zeros(size(Lfilter));
Lflat(ceil(10*FL):end) = msbackadj((ceil(10*FL)/FL:1/FL:length(Lfilter)/FL)', Lfilter(ceil(10*FL):end)', 'StepSize', W, 'windowsize', W,'SHOWPLOT',0);
Lbackground = Lfilter-Lflat;
Lfilter = Lflat./Lbackground;  %deltaF/F


%% Plot the overall trace

intro_id = strfind_part(behaviors, {'RFe'});
removal_id = strfind_part(behaviors, {'RFe'});
name = 'Sexual behavior';

% plot the curve under dF/F scale
GCamP_trace_norm2(Lfilter,Lfilter, t, FL, behaviors, Fstart, Fstop, intro_id(1), removal_id(end), {'Sniff','Mount','Intromission','Ejaculation'},name);

% plot the curve under Z-scored dF/F scale
Lz = (Lfilter - mean(Lfilter))/std(Lfilter);
GCamP_trace_norm2(Lz,Lz, t, FL, behaviors, Fstart, Fstop, intro_id(1), removal_id(end), {'Sniff','Mount','Intromission','Ejaculation'},name);
%% Plot the PSTH of a specific behavior
intro_id = strfind_part(behaviors, {'RFe'});
removal_id = strfind_part(behaviors, {'RFe'});
Lz = (Lfilter - mean(Lfilter))/std(Lfilter);

behaviorTest = 'Sniff';
GCamP_PSTH_raw_orz(Lz, t, FL, behaviors,Fstart,Fstop,behaviorTest,intro_id(1), removal_id(end), 'r');
end