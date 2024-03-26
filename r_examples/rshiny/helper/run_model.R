.libPaths(c("/cc-home/_global_/R/_global_/R/", .libPaths()))

run_model <- function(df, input_1, input_2) {
    library(cobs)
    library(magrittr)
    
    # load in model and feature engineering object
    feature_engineering_object <- readRDS("./model_object/feature_engineering_object.RDS")
    model_object <- readRDS("./model_object/model_object.RDS")

    # load from storage volume if needed
    #feature_engineering_object <- readRDS("/mnts/local1tb/ANZ/R-Deployment/feature_engineering_object.RDS")
    #model_object <- readRDS("/mnts/local1tb/ANZ/R-Deployment/model_object.RDS")

    # calculate engineered feature from cobs object
    df_out <- df %>%
        dplyr::mutate(
            engineered_input_1 = predict(feature_engineering_object, z = input_1)[, "fit"]
        )

    df_out <- df_out %>% dplyr::mutate(model_outcome = predict(model_object, newdata = df_out))

    return(df_out)
}
