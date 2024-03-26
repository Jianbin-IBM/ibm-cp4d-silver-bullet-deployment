# install specific version of xgboost to ensure the development and deployment environment have the same version

# install.packages("https://cloud.r-project.org/src/contrib/Archive/xgboost/xgboost_1.5.2.1.tar.gz", repos=NULL, type="source")
# Set the working directory to a specific folder

setwd("/userfs/code_examples/deploy_r_model")

library(xgboost)

data(iris)

species <- iris$Species
label <- as.integer(iris$Species) - 1
iris$Species <- NULL

n <- nrow(iris)
train.index <- sample(n, floor(0.75 * n))
train.data <- as.matrix(iris[train.index, ])
train.label <- label[train.index]
test.data <- as.matrix(iris[-train.index, ])
test.label <- label[-train.index]
xgb.train <- xgb.DMatrix(data = train.data, label = train.label)
xgb.test <- xgb.DMatrix(data = test.data, label = test.label)
num_class <- length(levels(species))

params <- list(
  booster = "gbtree",
  eta = 0.001,
  max_depth = 5,
  gamma = 3,
  subsample = 0.75,
  colsample_bytree = 1,
  objective = "multi:softprob",
  eval_metric = "mlogloss",
  num_class = num_class
)

model <- xgb.train(
  params = params,
  data = xgb.train,
  nrounds = 50,
  early_stopping_rounds = 3,
  watchlist = list(val1 = xgb.train, val2 = xgb.test),
  verbose = 0
)

xgb.save(model, "iris_xgb.model")