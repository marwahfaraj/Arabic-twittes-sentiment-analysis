from os import times
from flask import Flask, render_template
from flask import request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)
loaded_model = load_model('mlp_model.h5')
# with open('tfidf_model.joblib', 'r') as f:
word_vectorizer = joblib.load('tfidf_model.joblib')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/model', methods=['GET', 'POST'])
def model():
    inputs = request.args
    feature = []
    for key, val in inputs.items():
        feature.append(str(val))

    co_input = word_vectorizer.transform(feature)
    co_input.sort_indices()
    results = loaded_model.predict(co_input)
    if results >= 0.4:
        res = 'Postive_tweet'
    else:
        res = 'Negative_tweet'
    return jsonify(model_result=res)
