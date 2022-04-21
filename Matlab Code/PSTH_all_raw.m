%% Code used to generate the average PSTH from all the mice 

% Set Pathway
AnnFileB = A; 
BEF = 150;
AFT = 150;
timeIndex = 251:300;
allPSTH_raw_1 = nan(length(AnnFileB), BEF+AFT+1);
allPSTH_raw_2 = nan(length(AnnFileB), BEF+AFT+1);

behaviorDuration = nan(length(AnnFileB),1);
behaviorCount = nan(length(AnnFileB),1);
Color = 'rr'; 

behaviorOn = 'RFe';
behaviorOff = 'RFe';
behaviorTest = 'Ejaculation';

%% Calculate the mean PSTH from each animal
for i = 1: length(AnnFileB)
    %% Load Data
    matfile = regexprep(AnnFileB{i},'.txt','.mat');
    [Fstart, Fstop, behaviors] = inputtext(AnnFileB{i});
    load (matfile,'Lfilter', 'FL', 't','Lfilter2'); 
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
    
    %% Get the raw trace Onset and Offset
    intro_id = strfind_part(behaviors, {behaviorOn});
    removal_id = strfind_part(behaviors, {behaviorOff});
    
    [PSTH_raw_1, behaviorCount(i),behaviorDuration(i)] = GCamP_PSTH_raw_of(Lfilter, t, FL, behaviors, ...
        Fstart,Fstop, behaviorTest,intro_id(1), removal_id(end),'y','noo', BEF, AFT);
    [PSTH_raw_2, behaviorCount(i),behaviorDuration(i)] = GCamP_PSTH_raw_of(Lfilter2, t, FL, behaviors, ...
        Fstart,Fstop, behaviorTest,intro_id(1), removal_id(end),'y','noo', BEF, AFT);
    
    allPSTH_raw_1(i,:)= PSTH_raw_1;
    allPSTH_raw_2(i,:)= PSTH_raw_2;

end
%% Plotting
ylimit = [-2 6];

fig1 = figure();
hold on
plotwerror(-BEF/25:1/25:AFT/25, allPSTH_raw_1, [165 146 53]/255);
plotwerror(-BEF/25:1/25:AFT/25, allPSTH_raw_2, 'r');
hold on; plot([0,0],[-2,6],'--k','lineWidth',1);
set(gca,'Color','w','XColor','k','YColor','k','FontSmoothing','on','FontSize',15);
set(gcf,'Color','w');
set(gca, 'XTick', -6:6:6);
xlim([-6 6]);
ylabel('Z-socre','Color','k','FontSize',15);
xlabel('Time(s)','Color','k','FontSize',15);
ylim(ylimit);
fig1.InvertHardcopy = 'off';

fig2 = figure;
imagesc(allPSTH_raw_1)
set(gca, 'XTick', 0:125:500)
set(gca,'XTickLabel',{'-10','-5','0','5','10'})
colorbar
ylabel('Mice','Color','k','FontSize',15)
xlabel('Time(s)','Color','k','FontSize',15)
fig2.InvertHardcopy = 'off';

