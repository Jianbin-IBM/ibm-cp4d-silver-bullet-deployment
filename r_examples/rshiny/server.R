# .libPaths(c("/cc-home/_global_/R/_global_/R/", .libPaths()))

shinyServer(function(input, output, session) {
    observeEvent(input$manual_reset, {
        # reset input
        shinyjs::reset("input_1")
        shinyjs::reset("input_2")
    })


    # Manually type in company ratios
    input_df <- reactive({
        data <- data.frame(
            "input_1" = input$input_1,
            "input_2" = input$input_2
        )
        return(data)
    })

    # Run model with Preloaded ratios - integrated function will run through the "Financial + Qualatative + Country modules + Overlay module"
    result_df <- eventReactive(input$execute_model, {
        model_res <- run_model(input_df(),
            input_1 = input_1,
            input_2 = input_2
        )

        return(model_res)
    })

    # Send Model Outcome to UI
    output$model_result <- renderTable(
        {
            model_result <- result_df()

            return(model_result)
        },
        colnames = TRUE
    )

}) # end shinyServer
