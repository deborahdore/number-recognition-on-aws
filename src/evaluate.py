from os import path

from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from src.conf import BEST_MODEL_DIR
from src.utility import assemble_features


def evaluate_model(dataset):
    # load model
    if not path.isdir(BEST_MODEL_DIR):
        print("ERORR - not a valid directory")
        raise FileExistsError()

    model = PipelineModel.load(BEST_MODEL_DIR)

    # assemble pixels
    dataset = assemble_features(dataset)

    # eval
    evaluator = MulticlassClassificationEvaluator()
    evaluator.setPredictionCol("prediction")
    return evaluator.evaluate(model.transform(dataset))
