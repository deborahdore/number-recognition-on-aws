import pytesseract
from flask import Flask, render_template, request
from pyspark.sql import SparkSession

from src.conf import ACCESS_KEY, SECRET_KEY
from src.predict import predict_image
from src.utils import img_transform, to_dataframe

app = Flask(__name__, template_folder='./templates', static_folder="./static")


def load_PySpark():
    spark = SparkSession.builder \
        .config('spark.executor.memory', '6G') \
        .config('spark.driver.memory', '4G') \
        .config('spark.driver.maxResultSize', '5G') \
        .config('spark.debug.maxToStringFields', '50000') \
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.3.1') \
        .getOrCreate()

    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", '%s' % ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", '%s' % SECRET_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

    return spark


spark = load_PySpark()
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
