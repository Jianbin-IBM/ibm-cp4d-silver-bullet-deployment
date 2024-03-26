#!/usr/bin/env Rscript

# Load required libraries
library(xgboost)
library(jsonlite)

print('.libPaths() = ')
print(.libPaths())

# Read input from command line arguments
args <- commandArgs(trailingOnly = TRUE)

# Check if input is provided
if (length(args) == 0) {
  stop("Insufficient arguments.", call. = FALSE)
}

# Parse the JSON string
parsed_args <- fromJSON(args[1])

# Extract the input data fields and values
fields <- parsed_args$input_data$fields
values <- parsed_args$input_data$values

# Convert values to a data frame
df <- data.frame(values)

classes <- c("setosa", "versicolor", "virginica")
# Load the model
model <- xgb.load("iris_xgb.model")

# Make predictions
pred <- predict(model, as.matrix(df), reshape = TRUE)

# Convert predictions to a data frame
pred_df <- as.data.frame(pred)
# print('pred_df=')
# print(pred_df[1, ]) # first row
# print(pred_df)

# Set column names
colnames(pred_df) <- classes

# Calculate maximum probability and corresponding prediction
pred_df$probability <- apply(pred_df, 1, max)
pred_df$prediction <- apply(pred_df, 1, function(x) colnames(pred_df)[which.max(x)])

# print('prediction=')
# print(pred_df$prediction)

# Extract required fields
output_fields <- c("prediction_classes", "probability")

# Initialize an empty list to store the results
result_list <- list()

# Iterate over each row of the probability dataframe
for (i in 1:nrow(pred_df)) {
  # Combine the prediction with the corresponding row of the probability dataframe
  result_list[[i]] <- list(pred_df$prediction[i], pred[i, ])
}

# Convert predictions to JSON format
output_json <- toJSON(list(fields = output_fields, values = result_list))


# Print output to stderr
cat(output_json, file = stderr())