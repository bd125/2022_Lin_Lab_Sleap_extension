%% Code use to calculate the correlation coefficient
clc:clear;close all
A = {};
%% Set Pathway
AnnFileB = A; 
for i = 1:length(A)
%% Load Data
   matfile = AnnFileB{i};
   matfile = regexprep(AnnFileB{i},'.txt','.mat');
   
    load (matfile,'Lfilter', 'Lfilter2', 'FL', 't'); 
    if size(Lfilter, 2) ==1
        Lfilter = Lfilter';
    end
    W = floor(length(Lfilter)/FL/10);
    Lflat = zeros(size(Lfilter));
    Lflat(ceil(10*FL):end) = msbackadj((ceil(10*FL)/FL:1/FL:length(Lfilter)/FL)', ...
        Lfilter(ceil(10*FL):end)', 'StepSize', W, 'windowsize', W,'SHOWPLOT',0);
    Lbackground = Lfilter-Lflat;
    Lfilter = Lflat./Lbackground;  %deltaF/F
    if size(Lfilter2, 2) ==1
        Lfilter2 = Lfilter2';
    end
    W = floor(length(Lfilter2)/FL/10);
    Lflat = zeros(size(Lfilter2));
    Lflat(ceil(10*FL):end) = msbackadj((ceil(10*FL)/FL:1/FL:length(Lfilter2)/FL)', ...
        Lfilter2(ceil(10*FL):end)', 'StepSize', W, 'windowsize', W,'SHOWPLOT',0);
    Lbackground = Lfilter2-Lflat;
    Lfilter2 = Lflat./Lbackground; 

%% calculate the correlation coefficient for +-2s 
    correlationTemp = nan(1,11);
    a = 0;
    for j = -20:20
       a = a + 1;
        LWaveTemp = Lfilter (round(2*60*FL): round((12*60)*FL));
       LWave2Temp = Lfilter2 (round((2*60+j*0.1)*FL): round(( 12*60+ j*0.1)*FL));
       if length(LWaveTemp) > length(LWave2Temp)
            LWaveTemp = LWaveTemp(1: end -1);
       elseif length(LWaveTemp) < length(LWave2Temp)
            LWave2Temp = LWave2Temp(1: end -1);
       end
       r = corrcoef(LWaveTemp, LWave2Temp);
       correlationTemp(a) = r(2);
    end
allCorrelation_raw(i,:) = correlationTemp;
end
%%
fig1 = figure; 
hold on
plotwerror(-2:0.1:2, allCorrelation_raw(1:3,:), [134 134 134]/255);
hold on; plot([0,0],[-100,100],'--k','lineWidth',0.5)
set(gca,'Color','w','XColor','k','YColor','k','FontSmoothing','on','FontSize',15)
set(gcf,'Color','w')
ylabel('Correlation','Color','k','FontSize',15)
xlabel('Time(s)','Color','k','FontSize',15)
ylim([-0 1])
xlim([-2 2])
fig1.InvertHardcopy = 'off';

