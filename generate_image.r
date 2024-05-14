#!/bin/env R

library(httr)
library(jsonlite)

# read the arguments
args <- commandArgs(trailingOnly = TRUE)
lat = args[1]
lon = args[2]
outfile = args[3]
outfile_dim_x = 264
outfile_dim_y = 176

if( is.na(outfile) ){
    outfile = 'current_weather.png'
}

lat = "59.857958"
lon = "17.637296"
outfile = "current_weather.png"

# get the forecast
url  = paste0("https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=", lat, "&lon=", lon)
res  = GET(url)
json = rawToChar(res$content)
data_raw = fromJSON(json)

data = data.frame(data_raw$properties$timeseries$time, data_raw$properties$timeseries$data$instant$details$air_temperature, data_raw$properties$timeseries$data$instant$details$cloud_area_fraction, data_raw$properties$timeseries$data$next_1_hours$details$precipitation_amount)
colnames(data) = c("time", "temperature", "cloud_area", "rain")

# convert time column to time objects
data$time = strptime(data$time, format='%Y-%M-%dT%H:%M:%SZ')

# limit data to the coming 24h
data = data[1:26,]


### plot the data

# plot to png
png(file=outfile, width=outfile_dim_x, height=outfile_dim_y)

# init surface
par(mar=c(1.5,2.1,1.3,1))

# plot the precipitation
barplot(data$rain, xlab='', ylab='', bty='n', ylim=c(0, 3), axes=F, border=FALSE, col='#888888')

# plot the line on top of the boxes
par(new=TRUE)

# init plot surface
plot(1:length(data$time), data$temperature, type='n', xlab='', ylab='', bty='n', ylim=c(min(data$temperature)-(max(data$temperature)-min(data$temperature))*0.2, max(data$temperature)), axes=F)

# plot the temperature line
lines(1:length(data$time),data$temperature, col='black', lwd=3)


# plot the X axis
xlabels = c("", sprintf("%02d", data$time$hour[data$time$hour%%6==0]), "")
xat = c(0, which(data$time$hour%%6==0), length(data$temperature))
axis(side=1, at=xat, labels=xlabels, lwd=3, lend=1, cex.axis=1, padj=-0.8)


# plot the Y axis
yat = c(min(data$temperature)-(max(data$temperature)-min(data$temperature))*0.248, as.integer(seq(min(data$temperature), max(data$temperature), length.out=3)), max(data$temperature))
ylabels = c("", as.integer(seq(min(data$temperature), max(data$temperature), length.out=3)), "")
axis(side=2, at=yat, labels=ylabels, lwd=3, lwd.ticks=-1, lend=1, cex.axis=1.8, padj=0.5, las=1, hadj=0.63)



# add axis text
mtext("24h Forecast", 3, font=2, cex=1, padj=0, adj=0.5)
mtext(strftime(Sys.time(), "%y%m%d"), 3, font=2, cex=1, padj=0, adj=1.03)
mtext("t", 1, padj=0, adj=1.04)
mtext(expression(~degree~C), 2, padj=-8, adj=1.1, las=1, cex=1.05)

# box(lwd=3)


dev.off()






