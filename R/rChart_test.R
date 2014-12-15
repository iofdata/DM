
librar('rCharts', 'ramnathv')
df <- read.csv("C:\\Users\\tanhao\\Documents\\R\\type.1h.csv",header=FALSE,stringsAsFactors=FALSE)
colnames(df) <- c("date","1", "2","3","4","5","6","7","8","9","10")
transform(df, date = as.character(date))
for (i in c("1", "2","3","4","5","6","7","8","9","10")) {
  transform(df, i = as.numeric(i))
}
m1 <- mPlot(x = "date", y = c("1", "2","3","4","5","6","7","8","9","10"), type = "Line", data = df)
m1$set(pointSize = 0, lineWidth = 1)
m1$print("chart2")
m1

#base64enc
# install.packages("base64enc")
library("base64enc")
m1$save('C:\\Users\\tanhao\\Documents\\R\\graph1.html', 'inline', standalone=TRUE)


#librar('rCharts', 'ramnathv')
df <- read.csv("C:\\Users\\tanhao\\Documents\\R\\weibo.5m.csv",header=FALSE,stringsAsFactors=FALSE)
colnames(df) <- c("date","Sina", "Tenc")
transform(df, date = as.character(date))
m1 <- mPlot(x = "date", y = c("Sina", "Tenc"), type = "Line", data = df)
m1$set(pointSize = 0, lineWidth = 1)
m1$print("chart2")
m1

#base64enc
#install.packages("base64enc")
#library("base64enc")
m1$save('C:\\Users\\tanhao\\Documents\\R\\graph2.html', 'inline', standalone=TRUE)
