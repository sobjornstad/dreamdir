R_TRANSFER_FILE = 'dotplot-data.csv'
OUTPUT_LOCATION = 'graphs/'

minYear = 2011
maxYear = 2016

library(ggplot2)
library(scales)

cat("    Reading data...")
data <- read.csv(R_TRANSFER_FILE, sep=',', header=TRUE, stringsAsFactors=FALSE)
cat("done.\n")
cat("    Generating graph for years: ")
for (year in minYear:maxYear) {
    cat(year, ' ', sep='')
    data$month <- factor(data$month, labels=month.abb)
    data$lucid <- factor(data$lucid, labels=c("no", "yes"))
    qplot(month,day, data=data[data$year==year,],
          geom='point', size=numdreams, color=lucid,
          xlab="Month", ylab="Day",
          main=paste("Dream log entries in", year)) + 
          scale_x_discrete(drop=F) # show months with no dreams on graph
    fname <- paste(OUTPUT_LOCATION, year, "-recall-dotplot.svg", sep='')
    ggsave(filename=fname, width=8, height=5)
}
cat("\n")
