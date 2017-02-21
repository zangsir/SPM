setwd('C:/Users/zangs/Desktop/macAir2017Jan/cpp/mk_nopass_exp/mk_ng/')


#bigram 100p
bi100<-read.csv('bigram100p_rank_class.csv',header=TRUE)
library('ggplot2')

#save a plot as pdf for latex
pdf('rank_class_plot_b100.pdf')
p<-qplot(factor(quantile),data=bi100,geom="bar",fill=factor(class))
p+labs(x = "motif index rank quantile",title='rank_class_stacked_bar_bigram100p')
dev.off()





bi100<-read.csv('bigram200p_rank_class.csv',header=TRUE)
library('ggplot2')

#save a plot as pdf for latex
pdf('rank_class_plot_b200.pdf')
p<-qplot(factor(quantile),data=bi100,geom="bar",fill=factor(class))
p+labs(x = "motif index rank quantile",title='rank_class_stacked_bar_bigram100p')
dev.off()

#bigram 100p
bi100<-read.csv('trigram200p_rank_class.csv',header=TRUE)
library('ggplot2')

#save a plot as pdf for latex
pdf('rank_class_plot_t200.pdf')
p<-qplot(factor(quantile),data=bi100,geom="bar",fill=factor(class))
p+labs(x = "motif index rank quantile",title='rank_class_stacked_bar_bigram100p')
dev.off()

#bigram 100p
bi100<-read.csv('trigram300p_rank_class.csv',header=TRUE)
library('ggplot2')

#save a plot as pdf for latex
pdf('rank_class_plot_t300.pdf')
p<-qplot(factor(quantile),data=bi100,geom="bar",fill=factor(class))
p+labs(x = "motif index rank quantile",title='rank_class_stacked_bar_bigram100p')
dev.off()