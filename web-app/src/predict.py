from os import path

from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import DataFrame

from src.conf import BEST_MODEL_DIR, COLUMNS


def predict_image(input_from_web: DataFrame):
    if not path.isdir("../" + BEST_MODEL_DIR):
        print("ERORR - not a valid directory")
        raise FileExistsError()

    model = PipelineModel.load("../" + BEST_MODEL_DIR)

    assembler = VectorAssembler(inputCols=COLUMNS,
                                outputCol="features")

    features = assembler.transform(input_from_web).select("features")

    return model.transform(features)
