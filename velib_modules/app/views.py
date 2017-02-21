from flask import render_template, request, jsonify
from velib_modules.app import app
from velib_modules.api.predict import predict_available_bikes
from velib_modules.utils.io import load_pickle

import pandas as pd


# Todo: include Velib logo
# Todo: train new model
# Todo: Convert minutes in 1/6 of hour
# Todo: create module evaluate performance
# Todo: confidence interval

# Todo : handle errors in javascripts
# Todo: create tests

# Todo : create auth in api

# Todo : Store a model.pkl in the S3 bucket, and change the query accordingly
# Todo : Faire un package (setup.py)


# Load model
model = load_pickle("files/classic_model/model.pkl")

# Load list of stations
list_stations = pd.read_csv('files/input/list_stations.csv', encoding='utf-8')


# request example : curl -i http://localhost:5000/prediction/4006
@app.route('/prediction', methods=['POST'])
def ask_prediction():
    number_station = request.form['number_station']
    time_prediction = request.form["time_prediction"]
    prediction = predict_available_bikes(model, number_station, time_prediction)
    return jsonify({'prediction': prediction})


@app.route('/')
def index():
    number_station_index = 4006
    return render_template('prediction.html', list_stations=list_stations.values.tolist(),
                           number_station=number_station_index)
