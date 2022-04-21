function [PSTH_raw_On, behaviorCount,behaviorDuration] = GCamP_PSTH_raw_of(Lfilter, t, FL, behaviors, ...
        Fstart,Fstop, behavior,Pintro, Premove,color, EnablePlot, BEF, AFT)
    
if size(Lfilter, 2) ==1; Lfilter = Lfilter'; end

id = strfind_part(behaviors, {behavior});
if isempty(id)
    PSTH.filter = nan;
end

if nargin == 6; 
    Pintro = 0; 
    Premove = length(behaviors)+1;  
    color = 'k';
end

if nargin == 6; 
    color = 'k';
end

%% Get data 

Fstart_behavior = Fstart(id);
Fstop_behavior = Fstop(id);
for m =1:length(id)
    if ~isnan(id(m))
        for n = Fstart_behavior(m)-BEF:Fstart_behavior(m)+AFT
            PSTH.filter(m, n-(Fstart_behavior(m)-BEF)+1) = mean(Lfilter(floor(t(n-1)*FL):floor(t(n)*FL)));
        end
    end
end


%% Plot
if isequal(EnablePlot,'yes')
        fig1 = figure; hold on;
    for m =1:length(PSTH.filter(:,1))
        plot(-BEF/25:1/25:AFT/25, PSTH.filter(m,:), 'Color', [0.6, 0.6, 0.6], 'lineWidth', 1)
        if Fstop_behavior(m)-Fstart_behavior(m)<AFT
            plot((t(Fstop_behavior(m))-t(Fstart_behavior(m))), Lfilter(floor(t(Fstop_behavior(m))*FL)), 'k.');
        end
    end
    plot(-BEF/25:1/25:AFT/25, mean(PSTH.filter), color, 'lineWidth', 6)
    xlim([-6,6])

   
end



%% Return

PSTH_raw_On = mean(PSTH.filter, 1);
behaviorCount = length(id);
behaviorDuration = median(Fstop(id) - Fstart(id));


end