library(RNetLogo)
nlDir <- "C:/Program Files (x86)/NetLogo 5.1.0"
setwd(nlDir)

nl.path <- getwd()
NLStart(nl.path)

model.path <- "Z:/Windows.Documents/Desktop/Proj/Simulator - V2 Traffic/DC.nlogo"
NLLoadModel(model.path)


#NLCommand("setup-intelligents")
#NLSetAgentSet(agentset = "cars with [intelligent?]", input = 1111122222, var.name = "route")
#NLCommand("fix-int-route")
#NLDoCommandWhile("count cars = count cars with [color = green]","go", max.minutes = 1)
#NLDoCommand(1000,"go")
#NLReport("intel-time")

NLCommand("Initialize")

for (i in 1:500){
  for (j in 1:10){
    #NLCommand("load")
    NLCommand("do-go")
  }
  print(i)
  NLCommand("get-time")
  NLCommand("whiten")
  #print(NLReport("intel-times"))
}
