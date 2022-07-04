import sys

from pyspark.sql import *

from src.conf import DATASET_TRAIN, DATASET_TEST, ACCESS_KEY, SECRET_KEY
from src.evaluate import evaluate_model
from src.train import train_hypermodel


def load_PySpark():
    spark = SparkSession.builder \
        .config('spark.executor.memory', '6G') \
        .config('spark.driver.memory', '4G') \
        .config('spark.driver.maxResultSize', '5G') \
        .config('spark.debug.maxToStringFields', '50000') \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.1') \
        .getOrCreate()

    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", '%s' % ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", '%s' % SECRET_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    return spark


if __name__ == '__main__':

    print("Loading Spark")
    spark = load_PySpark()
    test_df = spark.read.csv(DATASET_TEST, inferSchema=True, header=True)
    train_df = spark.read.csv(DATASET_TRAIN, inferSchema=True, header=True)

    print("Dataset downloaded")

    # modality
    if len(sys.argv) < 2:
        print("Model training")
        train_hypermodel(train_df)
        print("Model evaluation")
        print(evaluate_model(test_df))
    else:
        mode = sys.argv[1]
        if mode == "train":
            train_hypermodel(train_df)
        elif mode == "evaluate":
            print(f"Model accuracy: {evaluate_model(test_df)}")
