import sys

import pandas as pd
from pyspark.sql import *
from src.evaluate import evaluate_model
from src.train import train_hypermodel

#DATASET_TRAIN = 'dataset/mnist_train.csv'
DATASET_TRAIN = 'https://cloud-project-adi.s3.amazonaws.com/mnist_train.csv'

#DATASET_TEST = 'dataset/mnist_test.csv'
DATASET_TEST = 'https://cloud-project-adi.s3.amazonaws.com/mnist_test.csv'



def load_PySpark():
    return SparkSession.builder \
        .config("spark.ui.port", "4050") \
        .config('spark.executor.memory', '4G') \
        .config('spark.driver.memory', '45G') \
        .config('spark.driver.maxResultSize', '10G') \
        .config('spark.debug.maxToStringFields', '50000') \
        .getOrCreate()


if __name__ == '__main__':

    spark = load_PySpark()
    test_df = spark.createDataFrame(pd.read_csv(DATASET_TEST))
    train_df = spark.createDataFrame(pd.read_csv(DATASET_TRAIN))

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
