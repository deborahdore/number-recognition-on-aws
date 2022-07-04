from pyspark.ml.feature import VectorAssembler

from .conf import COLUMNS


def assemble_features(dataframe):
    assembler = VectorAssembler(inputCols=COLUMNS,
                                outputCol="features")

    return assembler.transform(dataframe).select("features", "label")
