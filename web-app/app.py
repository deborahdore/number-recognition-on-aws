from flask import Flask, render_template
from pyspark.ml import PipelineModel

from main import load_PySpark

app = Flask(__name__)
spark = load_PySpark()
model = PipelineModel.load("../models/best_model")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def predict():
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    '''
    return render_template('index.html', prediction='ciao')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    print("Open browser on address http://localhost:5000")
