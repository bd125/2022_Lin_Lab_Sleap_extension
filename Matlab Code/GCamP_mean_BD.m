function X = GCamP_mean_BD(Lfilter, t, FL, behaviors, Fstart, Fstop, behavior, Pintro, Premove)

if size(Lfilter, 2) ==1; Lfilter = Lfilter'; end

if nargin == 7
    Pintro = 0;
    Premove = length(behaviors)+1; 
end

id = find(strcmp(behaviors, behavior));
if isempty(id)
    M = nan; B = nan;
end


id = id(id>Pintro & id<Premove);

diff = Fstop(id) - Fstart(id);

idIndex = find((diff > 25*0) ); 
% if length(idIndex)>16
%     id = id(idIndex(1:16));
% end


%% Mount only
% id = id(id>Pintro & id<Premove);
% d = 0;
% for i = 1:length(id)
%     if ismember({'Retrive'},behaviors(id(i)+1))
%             d = [d;i];
%     end
% end
% id(d(2:length(d))) = [];
% id = id(d(2:length(d)));

for m =1:length(id)
    if ~isnan(id(m))
       M(m) = mean(Lfilter(floor(t(Fstart(id(m)))*FL):floor((t(Fstop(id(m))))*FL)));  % mean value
    else
       M(m) = nan; B(m) = nan;
    end
end

X = M;