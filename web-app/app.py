import pytesseract
from flask import Flask, render_template, request
from pyspark.ml import PipelineModel

from main import load_PySpark
from src.predict import predict_image
from src.utils import img_transform, to_dataframe

app = Flask(__name__, template_folder='templates')
spark = load_PySpark()
model = PipelineModel.load("../models/best_model")
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def predict():
    global spark
    try:
        img_to_arr = img_transform(request.files['file'])
        df = to_dataframe(img_to_arr, spark)
        predicted_num = int(predict_image(df))
        return render_template('index.html', prediction=predicted_num)
    except Exception:
        # reload spark
        spark.stop()
        spark = load_PySpark()
        return render_template('index.html', prediction='Please upload another picture')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    print("Open browser on address http://localhost:5000")
