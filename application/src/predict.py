from os import path

from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler

from src.conf import BEST_MODEL_DIR, COLUMNS


def predict_image(df):
    if not path.isdir(BEST_MODEL_DIR):
        print("ERORR - not a valid directory")
        raise FileExistsError()

    model = PipelineModel.load(BEST_MODEL_DIR)

    assembler = VectorAssembler(inputCols=COLUMNS,
                                outputCol="features")

    features = assembler.transform(df).select("features")

    return model.transform(features).select('prediction').collect()[0][0]
