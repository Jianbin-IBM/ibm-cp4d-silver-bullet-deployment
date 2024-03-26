# .libPaths(c("/cc-home/_global_/R/_global_/R/", .libPaths()))
source("./helper/run_model.R")

ui <-
    shinyUI(
        fluidPage(
            shinyjs::useShinyjs(),
            # Include ANZ global styles
            tags$head(HTML("<link rel='stylesheet' type='text/css' href='main.css'>")),
            tags$head(HTML("<link rel='stylesheet' type='text/css' href='custom.css'>")),
            tags$head(HTML("<script type='text/javascript' src='sus6pzy.js'></script>")),
            tags$head(tags$style(HTML("hr {border-top: 1px solid #B0C4DE;}"))),
            # Banner
            tags$header(div(class = "primary clearfix", a(class = "logo", title = "ANZ Logo", "ANZ"))),
            # Application title
            tags$div(class = "hero", h2(class = "text--white", "Dummy App")),

            #---------------------------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------------------------
            tabsetPanel(
                id = "inTabset",

                #---------------------------------------------------------------------------------------------------------------------------------------
                # Tab: Manual Input
                #---------------------------------------------------------------------------------------------------------------------------------------
                tabPanel(
                    title = h4(strong("Execute Model: Manual Inputs")),
                    br(),
                    fluidRow(column(
                        12,
                        wellPanel(
                            tags$div(
                                tags$ul(
                                    tags$li("This tab executes the proposed model for the set of inputs below."),
                                    tags$li("Input values should be manually entered before executing the model.")
                                )
                            ),
                            fluidRow(
                                column(
                                    4,
                                    actionButton(
                                        inputId = "execute_model",
                                        label = "Execute Model"
                                    )
                                ),
                                column(8,
                                    style = "color:blue",
                                    tableOutput("model_result")
                                )
                            ),
                            fluidRow(column(
                                4,
                                actionButton("manual_reset", "Reset")
                            ))
                        )
                    )),
                    hr(),
                    br(),
                    h4(strong("Model Input")),
                    br(),


                    # Ratios Row 1
                    fluidRow(
                        conditionalPanel(
                            condition = TRUE,
                            column(
                                4,
                                numericInput(
                                    inputId = "input_1",
                                    label = h5("Input 1"),
                                    value = NULL,
                                    step = 0.000001
                                ),
                                div(style = "margin-top:-20px")
                            )
                        ),
                        conditionalPanel(
                            condition = TRUE,
                            column(
                                4,
                                numericInput(
                                    inputId = "input_2",
                                    label = h5("Input 2"),
                                    value = NULL,
                                    step = 0.000001
                                ),
                                div(style = "margin-top:-20px")
                            )
                        )
                    ),
                    br(),
                    hr()
                ) # End of Tab "Manual input"

                #---------------------------------------------------------------------------------------------------------------------------------------
            )
        ) # End fluidPage
    ) # End ShinyUI
