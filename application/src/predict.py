from pyspark.ml import PipelineModel
from pyspark.ml.feature import VectorAssembler

from .conf import BEST_MODEL_DIR, COLUMNS


def predict_image(df):
    try:

        model = PipelineModel.load(BEST_MODEL_DIR)

        assembler = VectorAssembler(inputCols=COLUMNS,
                                    outputCol="features")

        features = assembler.transform(df).select("features")

        return model.transform(features).select('prediction').collect()[0][0]

    except Exception:
        raise Exception("Model not found")
