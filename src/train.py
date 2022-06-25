from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import PCA, StandardScaler
from pyspark.ml.tuning import ParamGridBuilder, TrainValidationSplit

from src.conf import BEST_MODEL_DIR
from src.utility import assemble_features


def train_hypermodel(train):
    train_df = assemble_features(train)

    scaler = StandardScaler(inputCol="features",
                            outputCol="std_features",
                            withStd=True, withMean=True)

    # run PCA to extract features with higher variance
    pca_model = PCA(k=10, inputCol="std_features", outputCol="pca_features")

    lr = LogisticRegression(maxIter=150)

    # search for best hyperparamters
    param_grid = ParamGridBuilder() \
        .addGrid(lr.regParam, [0.1, 0.01]) \
        .addGrid(lr.fitIntercept, [False, True]) \
        .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0]) \
        .build()

    tvs = TrainValidationSplit(estimator=lr,
                               estimatorParamMaps=param_grid,
                               evaluator=MulticlassClassificationEvaluator(),
                               trainRatio=0.7)

    pipeline = Pipeline(stages=[scaler, pca_model])

    tvs_model = tvs.fit(pipeline.fit(train_df).transform(train_df)).bestModel

    new_pipeline = Pipeline(stages=[scaler, pca_model, tvs_model])

    new_pipeline.fit(train_df).write().overwrite().save(BEST_MODEL_DIR)
