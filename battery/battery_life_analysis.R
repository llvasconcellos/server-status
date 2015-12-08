setwd('/Users/robinedwards/Documents/MSF/Buendia/server-status/battery')

datain = read.csv('battery_data.csv', header=T)

combined = do.call('rbind', lapply(1:ncol(datain), FUN = function(i){
  d = na.omit(datain[, i])
  d = data.frame(t = 1:length(d)/6, bat = d)
  
  # initial model to estimate time when battery was 100%
  lm = lm(t ~ bat, data=d)
  pred = predict.lm(lm, newdata=data.frame(bat=c(100,0)), se.fit = TRUE)
  d$t_adj = d$t - pred$fit[1]
  d$id = ordered(names(datain)[i], levels=names(datain))
  return(d)
}))

if(require(ggplot2)){
  plt = ggplot(combined, aes(t_adj, bat, group=id, col=factor(id))) + 
    geom_line(size=1) + expand_limits(x = 0) + scale_y_continuous(limits = c(0,100)) +
    labs(x = 'time (hours)', y = 'charge (%)', 
         title = 'Battery Analysis', col = 'Session')
  ggsave(plt, file='battery_analysis_plot.pdf', w=6, h=4)
}

# combined model
f = lm(t_adj ~ bat, data=combined)
p = predict.lm(f, newdata=data.frame(bat=c(100,0)), se.fit = TRUE)
life = diff(p$fit)
# estimated battery duration

print(paste('Estimated duration', formatC(life, digits = 3), 'hours'))
