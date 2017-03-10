library(igraph)
library(rJava)
library(RNetLogo)
nlDir <- "C:\Users\wang-grad\Desktop\IADM\Project"
setwd(nlDir)

nl.path <- getwd()
NLStart(nl.path)

model.path <- file.path("CAAV-V2.nlogo")
NLLoadModel(file.path(nl.path, model.path))

#NLCommand("set density 70")    # set density value
#NLCommand("setup")             # call the setup routine 
#NLCommand("go")                # launch the model from R


library(ggplot2)
NLCommand("set density 60")
NLCommand("setup")
burned <- NLDoReportWhile("any? turtles", "go",
                          c("ticks", "(burned-trees / initial-trees) * 100"),
                          as.data.frame = TRUE, df.col.names = c("tick", "percent.burned"))
# Plot with ggplot2
p <- ggplot(burned,aes(x=tick,y=percent.burned))
p + geom_line() + ggtitle("Non-linear forest fire progression with density = 60")