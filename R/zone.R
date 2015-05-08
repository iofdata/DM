library('rCharts', 'ramnathv')
df <- read.csv("/Users/buttonwood/Downloads/dev/uniq/stat/type/zone.csv",header=FALSE,stringsAsFactors=FALSE,sep = " ")
colnames(df) <- c("value","type","zone")
n1 <- nPlot(value ~ type, group = "zone", data = df, type = "multiBarChart",rotateLabels=-45)
n1$print("type-zone1")
n1

n2 <- nPlot(value ~ zone, group = "index", data = df, type = "multiBarChart")
n2$print("type-zone2")
n2

library("base64enc")
n1$save('type-zone1.html', 'inline', cdn=FALSE)
n2$save('type-zone2.html', 'inline', cdn=FALSE)library('rCharts', 'ramnathv')
df <- read.csv("/Users/buttonwood/Downloads/dev/uniq/stat/type/zone.csv",header=FALSE,stringsAsFactors=FALSE,sep = " ")
colnames(df) <- c("value","type","zone")
n1 <- nPlot(value ~ type, group = "zone", data = df, type = "multiBarChart",rotateLabels=-45)
n1$print("type-zone1")
n1

n2 <- nPlot(value ~ zone, group = "index", data = df, type = "multiBarChart")
n2$print("type-zone2")
n2

library("base64enc")
n1$save('type-zone1.html', 'inline', cdn=FALSE)
n2$save('type-zone2.html', 'inline', cdn=FALSE)
