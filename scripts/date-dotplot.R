R_TRANSFER_FILE = 'dotplot-data.csv'
OUTPUT_LOCATION = '../graphs/'

minYear = 2011
maxYear = 2016

library(ggplot2)
library(scales)

data <- read.csv(R_TRANSFER_FILE, sep=',', header=TRUE, stringsAsFactors=FALSE)
for (year in minYear:maxYear) {
    data$month <- factor(data$month, labels=month.abb)
    qplot(month,day, data=data[data$year==year,],
          geom='point', size=numdreams,
          xlab="Month", ylab="Day",
          main=paste("Dream log entries in", year))
    fname <- paste(OUTPUT_LOCATION, year, "-recall-dotplot.svg", sep='')
    ggsave(filename=fname, width=8, height=5)
}
