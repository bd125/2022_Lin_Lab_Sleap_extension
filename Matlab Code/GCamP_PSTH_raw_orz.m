function [PSTH, line]= GCamP_PSTH_raw_orz(Lfilter, t, FL, behaviors, Fstart, Fstop, behavior, Pintro, Premove, color)

if size(Lfilter, 2) ==1; Lfilter = Lfilter'; end
BEF = 250; AFT = 250; 

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
fig1 = figure; hold on;

c = [0.6, 0.6, 0.6];

for m = 1:length(id)
    plot(-BEF/25:1/25:AFT/25, PSTH.filter(m,:), 'Color', c, 'lineWidth', 1)
    if Fstop_behavior(m)-Fstart_behavior(m)<AFT
        plot((t(Fstop_behavior(m))-t(Fstart_behavior(m))), Lfilter(floor(t(Fstop_behavior(m))*FL)), 'k.','MarkerSize',8);
    end
end
plot(-BEF/25:1/25:AFT/25, mean(PSTH.filter), color, 'lineWidth', 2)
line = mean(PSTH.filter);

ylabel('dF/F','Color','k','FontSize',15)
xlabel('Time(s)','Color','k','FontSize',15)
set(gca,'Color','w','XColor','k','YColor','k','FontSmoothing','on','FontSize',15)
set(gcf,'Color','w')
fig1.InvertHardcopy = 'off';
xlim([-10,10])

fig2 = figure; 
imagesc(PSTH.filter)
set(gca, 'XTick', 0:50:500)
set(gca,'XTickLabel',{'-10','-8', '-6', '-4', '-2','0','2','4','6','8','10'})
colorbar



end