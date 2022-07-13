from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import PCA, StandardScaler
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql import *

COLUMNS = ['pixel{:d}'.format(k) for k in range(784)]

S3_BUCKET_NAME = "number-recognition-on-aws-bucket"
ACCESS_KEY = "XXX"
SECRET_KEY = "XXX"

BEST_MODEL_DIR = f's3a://{S3_BUCKET_NAME}/models'

DATASET_TRAIN = f's3a://{S3_BUCKET_NAME}/mnist_train.csv'
DATASET_TEST = f's3a://{S3_BUCKET_NAME}/mnist_test.csv'


def load_PySpark():
    # when executing on amazon EMR
    # spark = SparkSession.builder.getOrCreate()

    # when executing local

    spark = SparkSession.builder \
        .config('spark.executor.memory', '6G') \
        .config('spark.driver.memory', '4G') \
        .config('spark.driver.maxResultSize', '5G') \
        .config('spark.debug.maxToStringFields', '50000') \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.1') \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3a.access.key", '%s' % ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3a.secret.key", '%s' % SECRET_KEY)

    spark.sparkContext._jsc.hadoopConfiguration().set(
        "fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    return spark


def assemble_features(dataframe):
    assembler = VectorAssembler(inputCols=COLUMNS,
                                outputCol="features")

    return assembler.transform(dataframe).select("features", "label")


def evaluate_model(dataset):
    try:
        model = PipelineModel.load(BEST_MODEL_DIR)
        # assemble pixels
        dataset = assemble_features(dataset)

        # eval
        evaluator = MulticlassClassificationEvaluator()
        evaluator.setPredictionCol("prediction")
        return evaluator.evaluate(model.transform(dataset))

    except Exception:
        print("Model does not exists")


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

    tvs = CrossValidator(estimator=lr,
                         estimatorParamMaps=param_grid,
                         evaluator=MulticlassClassificationEvaluator(),
                         numFolds=5)

    pipeline = Pipeline(stages=[scaler, pca_model])

    tvs_model = tvs.fit(pipeline.fit(train_df).transform(train_df)).bestModel

    new_pipeline = Pipeline(stages=[scaler, pca_model, tvs_model])

    new_pipeline.fit(train_df).write().overwrite().save(BEST_MODEL_DIR)

    print("--- MODEL SAVED ---")


if __name__ == '__main__':
    print("--- LOADING SPARK ---")

    spark = load_PySpark()
    print("--- SPARK LOADED ---")

    print("--- DOWNLOADING DATASET --- ")
    test_df = spark.read.csv(DATASET_TEST, inferSchema=True, header=True)
    train_df = spark.read.csv(DATASET_TRAIN, inferSchema=True, header=True)

    print("--- DATASET DOWNLOADED ---")

    print("--- MODEL TRAINING ---")
    train_hypermodel(train_df)

    print(f"--- MODEL EVALUATION: {evaluate_model(test_df)}")
