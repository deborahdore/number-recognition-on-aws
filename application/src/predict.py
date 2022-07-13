from pyspark.ml.feature import VectorAssembler

from .conf import COLUMNS


def predict_image(df, model):
    assembler = VectorAssembler(inputCols=COLUMNS,
                                outputCol="features")

    features = assembler.transform(df).select("features")

    return model.transform(features).select('prediction').collect()[0][0]
