# .libPaths(c("/cc-home/_global_/R/_global_/R/", .libPaths()))

library(cobs)
library(dplyr)
library(janitor)

# dummy dataset
data(iris)
clean_iris <- iris %>%
    janitor::clean_names() %>%
    dplyr::rename(
        input_1 = petal_width,
        input_2 = petal_length,
        target = sepal_length
    )


# Create a dummy feature engineering object
# fit a curve between the two variables
feature_engineering_object <- cobs::cobs(clean_iris$input_1, clean_iris$target)

# save the feature engineering object as RDS
saveRDS(feature_engineering_object, "./model_object/feature_engineering_object.RDS")

# Create a dummy object
model_object <- lm(target ~ engineered_input_1 + input_2,
    data = clean_iris %>%
        dplyr::mutate(engineered_input_1 = predict(feature_engineering, z = input_1)[, "fit"])
)

saveRDS(model_object, "./model_object/model_object.RDS")
