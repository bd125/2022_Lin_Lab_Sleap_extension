function plotwerror(xx,yy,coll)
hold on
ymean=nanmean(yy);
 

[a,b]=size(yy);
for c=1:b
    se_s(c)=sqrt(length(find(~isnan(yy(:,c)))));

        se(c)=nanstd(yy(:,c));


end
 
yse=se./se_s;
% yse=se; 
plot(xx,ymean,'color',coll,'linewidth',1.5)
% hold on
% plot(xx,ymean+yse,(coll),'linewidth',1)
% hold on
% plot(xx,ymean-yse,(coll),'linewidth',1)
 

xxU=(ymean+yse);
xxL=(ymean-yse);
jbfill(xx,xxU,xxL,coll,coll,1,0.25)