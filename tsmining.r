library(ggplot2)
library(TSMining)
data(BuildOperation)
ggplot(data = BuildOperation, aes(x = 1:dim(BuildOperation)[1], y = WCC)) +
geom_line() + geom_point()
ggplot(data = BuildOperation, aes(x = 1:dim(BuildOperation)[1], y = AHU)) +
geom_line() + geom_point()



#motif discovery
#ftp://cran.r-project.org/pub/R/web/packages/TSMining/vignettes/MotifDiscovery.html
res.wcc <- Func.motif(ts = BuildOperation$WCC, global.norm = T, local.norm = F, window.size = 24, overlap = 0, w = 6, a = 5, mask.size = 5, max.dist.ratio = 1.2, count.ratio.1 = 1.1, count.ratio.2 = 1.1)


#plot motifs in entire TS: WCC 
library(ggplot2)
#Visualization
data.wcc <- Func.visual.SingleMotif(single.ts = BuildOperation$WCC, window.size = 24, motif.indices = res.wcc$Indices)
data.ahu <- Func.visual.SingleMotif(single.ts = BuildOperation$AHU, window.size = 24, motif.indices = res.ahu$Indices)

#Determine the total number of motifs discovered in the time series of WCC
n <- length(unique(data.wcc$data.1$Y))
#Make the plot
ggplot(data = data.wcc$data.1) +  
    geom_line(aes(x = 1:dim(data.wcc$data.1)[1], y = X)) +
    geom_point(aes(x = 1:dim(data.wcc$data.1)[1], y = X, color=Y, shape=Y))+
    scale_shape_manual(values = seq(from = 1, to = n)) +
    guides(shape=guide_legend(nrow = 2)) +
    xlab("Time (15-min)") + ylab("WCC Power Consumption (kW)") +
    theme(panel.background=element_rect(fill = "white", colour = "black"),
          legend.position="top",
          legend.title=element_blank())



#WCC motifs
for(i in 1:length(data.wcc$data.2)) {
    data.temp <- data.wcc$data.2[[i]]
    print(ggplot(data = data.temp) +  
        geom_line(aes(x = Time, y = Value, color=Instance, linetype=Instance)) +
        xlab("Time (15-min)") + ylab("WCC Power Consumption (kW)") + ggtitle(paste0("WCC Motif ",i)) +
        scale_y_continuous(limits=c(0,max(data.temp$Value))) +
        theme(panel.background=element_rect(fill = "white", colour = "black"),
              legend.position="none",
              legend.title=element_blank()))    
}