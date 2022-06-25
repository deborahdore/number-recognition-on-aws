from os import path

from pyspark.ml import PipelineModel
from pyspark.sql import DataFrame

from src.conf import BEST_MODEL_DIR
from src.utility import assemble_features


def predict_image(input_from_web: DataFrame):
    if not path.isdir(BEST_MODEL_DIR):
        print("ERORR - not a valid directory")
        raise FileExistsError()

    model = PipelineModel.load(BEST_MODEL_DIR)

    features = assemble_features(input_from_web)

    return model.transform(features)
