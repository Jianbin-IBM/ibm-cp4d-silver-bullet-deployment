#!/usr/bin/env Rscript

# for Online API, main R must be able to process input json and then generate output json
library(xgboost)
library(jsonlite)

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
  stop("Insufficient arguments.", call. = FALSE)
}

# Parse the JSON string
parsed_args <- fromJSON(args[1])

# Extract the "inputs" list
data <- parsed_args$input_data$values[[1]]$inputs
df <- data.frame(data)
colnames(df) <- data$fields

classes <- c("setosa", "versicolor", "virginica")
model <- xgb.load("iris_xgb.model")
pred <- predict(model, as.matrix(df), reshape=T)

pred <- as.data.frame(pred)
colnames(pred) <- classes

pred$probability <- apply(pred, 1, function(x) max(x))
pred$prediction <- apply(pred, 1, function(x) colnames(pred)[which.max(x)])

# output_json <- toJSON(pred)

output_json <- toJSON(list(values = pred))

#### Print output_json to stderr
# reason: stdout will contain all the print from the code, which will interfere the output_json
# when nothing wrong, stderr will give us a clean output_json
# when sth wrong, we won't have correct output_json anyway and stderr will be used to indicate the error msg
cat(output_json, file = stderr())