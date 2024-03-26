#  .libPaths(c("/cc-home/_global_/R/_global_/R/", .libPaths()))


library(shinyjs)
library(shinyalert)
library(shinyWidgets)
library(grDevices)
source("./helper/run_model.R")

# source all R scripts
source("ui.R")
source("server.R")

# start the shiny app
shiny::shinyApp(ui = ui, server = server)