import sys

from pyspark.sql import *

from src.evaluate import evaluate_model
from src.train import train_hypermodel

DATASET_TRAIN = 's3a://cloud-project-adi/mnist_test.csv'

DATASET_TEST = 's3a://cloud-project-adi/mnist_test.csv'


def load_PySpark():
    spark = SparkSession.builder \
        .config("spark.ui.port", "4050") \
        .config('spark.executor.memory', '4G') \
        .config('spark.driver.memory', '45G') \
        .config('spark.driver.maxResultSize', '10G') \
        .config('spark.debug.maxToStringFields', '50000') \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.1') \
        .getOrCreate()

    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", '**')
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", '****')
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    return spark


if __name__ == '__main__':

    spark = load_PySpark()
    test_df = spark.read.csv(DATASET_TEST, inferSchema=True, header=True)
    train_df = spark.read.csv(DATASET_TRAIN, inferSchema=True, header=True)

    # modality
    if len(sys.argv) < 2:
        train_hypermodel(train_df)
        print(evaluate_model(test_df))
    else:
        mode = sys.argv[1]
        if mode == "train":
            train_hypermodel(train_df)
        elif mode == "evaluate":
            print(evaluate_model(test_df))
