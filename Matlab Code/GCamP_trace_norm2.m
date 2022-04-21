function GCamP_trace_norm2(Lfilter, Lfilter2,t, FL, behaviors, Fstart, Fstop, Pintro, Premove, types,name)

if size(Lfilter, 2) ==1; Lfilter = Lfilter'; end
BEF = 10; AFT = 100;

if nargin ==6
    Pintro = 1; 
    Premove = length(behaviors); 
    types = unique(behaviors(Pintro:Premove));
    BEF = 0; AFT = 0; 
end

if nargin ==8
    types = unique(behaviors(Pintro:Premove));
end    


Tstart = t(Fstart(Pintro))-BEF; 
Tstop = t(Fstop(Premove))+AFT; 
Lplot = Lfilter(floor(Tstart*FL)+1:min(length(Lfilter), floor(Tstop*FL)));
Lplot2 = Lfilter2(floor(Tstart*FL)+1:min(length(Lfilter), floor(Tstop*FL)));

temp = strfind_part(types, {'baseline', 'other','between'});
ci = setdiff(1:(length(types)+1), temp);
colors = distinguishable_colors(min(10, length(types)-length(temp)+1), {'b','k','w','g'});
colors(ci,:) = colors; 
colors(temp,:) = ones(length(temp),3);
fig1 = figure; hold on
for j = 1:length(types)    
     c = colors(j,:); 
    id = find(strcmp(types{j}, behaviors));
    id = id(t(Fstart(id))>=Tstart & t(Fstop(id))<=Tstop);
    
    for i = 1:length(id)
        hh(j)=area([t(Fstart(id(i)))-Tstart-BEF,t(Fstop(id(i)))-Tstart-BEF], [min(Lplot)+(max(Lplot)-min(Lplot))/3,min(Lplot)+(max(Lplot)-min(Lplot))/3],min(Lplot), 'Edgecolor', 'none', 'Facecolor', c);
        child=get(hh(j),'Children');
        set(child,'FaceAlpha',0.6) ;
    end
end
h = hh(hh~=0); 
types = types(hh~=0); 

tplot = -BEF+1/FL:1/FL:length(Lplot)/FL-BEF;
plot(tplot, Lplot, 'Color','g','lineWidth',1);
plot(tplot, Lplot2,'Color','b','lineWidth',1);
plot([0, 0], [min(Lplot), max(Lplot)], 'r--');
plot([t(Fstop(Premove))-t(Fstart(Pintro)), t(Fstop(Premove))-t(Fstart(Pintro))], [min(Lplot), max(Lplot)], 'r--');

set(gca,'Color','w','XColor','k','YColor','k','FontSize',15)
set(gcf,'Color','w')
ylabel('Z-score','Color','k','FontSize',15)
xlabel('Time (s)','Color','k','FontSize',15)
fig1.InvertHardcopy = 'off';




title(name)
