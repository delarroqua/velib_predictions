from flask import render_template, request # jsonify
from velib_predictions.app.predict import *
from velib_predictions.app import app
from velib_predictions.utils.io import load_pickle

# Load model
model = load_pickle("files/model.pkl")

# request example : curl -i http://localhost:5000/velib/api/prediction/4006
#@app.route('/velib/api/prediction/<int:number_station>', methods=['GET'])
#def ask_prediction(number_station):
@app.route('/velib/api/prediction', methods=['POST'])
def ask_prediction():
    number_station = request.form['number_station']
    prediction = predict_available_bikes(model, number_station)
    return render_template('prediction.html', number_station=number_station, prediction=prediction)
    #return jsonify({'prediction': prediction})


@app.route('/')
def index():
    return render_template('prediction.html')
