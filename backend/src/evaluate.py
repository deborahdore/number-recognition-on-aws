from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from .conf import BEST_MODEL_DIR
from .utility import assemble_features


def evaluate_model(dataset):
    try:
        model = PipelineModel.load(BEST_MODEL_DIR)
        # assemble pixels
        dataset = assemble_features(dataset)

        # eval
        evaluator = MulticlassClassificationEvaluator()
        evaluator.setPredictionCol("prediction")
        return evaluator.evaluate(model.transform(dataset))

    except Exception:
        print("Model does not exists")
