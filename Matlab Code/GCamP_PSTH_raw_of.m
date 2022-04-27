function [PSTH_raw_On,PSTH_raw_Off, behaviorCount,behaviorDuration] = GCamP_PSTH_raw_of(Lfilter, t, FL, behaviors, ...
        Fstart,Fstop, behavior,Pintro, Premove,color, EnablePlot, BEF, AFT)
    
if size(Lfilter, 2) ==1; Lfilter = Lfilter'; end

%id = find(strcmp(behaviors, behavior));
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

%%
% 
% %get clean trisl
% if (sum(strcmp({'Sniff'}, behavior)))>0
%     id = id(id>Pintro & id<Premove);
%     social_id = strfind_part(behaviors, {'Sniff'});
%     diff = Fstart(social_id(2:end))-Fstop(social_id(1:end-1));
%     clean = [social_id(1), social_id(find(diff>25*5)+1)];  % set the number of spacing frames between two social events
%     id = intersect(id, clean);
% else
%     id = id(id>Pintro & id<Premove);
% end




% Get behaviors longer than 2.5s
id = id(id>Pintro & id<Premove);

diff = Fstop(id) - Fstart(id);
idIndex = find((diff > 25*0) ); %(diff > 25*35)& (diff < 25*60)
id = id(idIndex);

% if length(idIndex)<=30
%     id = id;
% else
%     id = id(1:30);
% end

% % Mount only
% id = id(id>Pintro & id<Premove);
% d = 0;
% for i = 1:length(id)
%     if ismember({'Intromission'},behaviors(id(i)+1))
%             d = [d;i];
%     end
% end
% id(d(2:length(d))) = [];
% id = id(d(2:length(d)));
% id = id(round(length(id)/2):end);

%% Get data 

Fstart_behavior = Fstart(id);
Fstop_behavior = Fstop(id);

for m =1:length(id)
    if ~isnan(id(m))
        for n = Fstart_behavior(m)-BEF:Fstart_behavior(m)+AFT
            PSTH.filter(m, n-(Fstart_behavior(m)-BEF)+1) = mean(Lfilter(floor(t(n-1)*FL):floor(t(n)*FL)));%Lfilter(floor(t(approach_Fstart(m)+BEF)*FL));
        end
    end
    %PSTH.filter(m,:) = PSTH.filter(m,:)-mean(PSTH.filter(m, BEF-10:BEF-5));
end

Fstart_behavior = Fstop(id);
for m =1:length(id)
    if ~isnan(id(m))
        for n = Fstart_behavior(m)-BEF:Fstart_behavior(m)+AFT
            PSTH2.filter(m, n-(Fstart_behavior(m)-BEF)+1) = mean(Lfilter(floor(t(n-1)*FL):floor(t(n)*FL)));%Lfilter(floor(t(approach_Fstart(m)+BEF)*FL));
        end
    end
    %PSTH.filter(m,:) = PSTH.filter(m,:)-mean(PSTH.filter(m, BEF-10:BEF-5));
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
%     ylim([-0.05 0.4])
    xlim([-6,6])
%     savefig(fig1,name)
%     
%     fig2 = figure; 
%     imagesc(PSTH.filter)
%     set(gca, 'XTick', 0:50:500)
%     set(gca,'XTickLabel',{'-10','-8', '-6', '-4', '-2','0','2','4','6','8','10'})
%     colorbar
%     title(['Heatmap ' name])
%     spathway = ['Heatmap ' name];
%     savefig(fig2,spathway)
   
end



%% Return

PSTH_raw_On = mean(PSTH.filter, 1);
PSTH_raw_Off = mean(PSTH2.filter, 1);
behaviorCount = length(id);
behaviorDuration = mean(Fstop(id) - Fstart(id));


end