from flask import render_template, request, jsonify, redirect
from velib_modules.app import app
from velib_modules.api.predict import predict_available_bikes
from velib_modules.utils.io import load_pickle, load_json

import pandas as pd
import os



# Todo : handle errors in javascripts

# Todo: create tests
# Todo : create auth in api


# Load model
path_model = "files/app_model/"
model = load_pickle(os.path.join(path_model, 'model.pkl'))

# Load list of stations
list_stations = pd.read_csv('files/input/list_stations.csv', encoding='utf-8')


# request example : curl -i http://localhost:5000/prediction/4006
@app.route('/prediction', methods=['POST'])
def ask_prediction():
    number_station = request.form['number_station']
    time_prediction = request.form["time_prediction"]
    available_bikes, bike_stands = predict_available_bikes(model, number_station, time_prediction)
    return jsonify({'available_bikes': available_bikes, 'bike_stands': bike_stands})


@app.route('/feedback', methods=['POST'])
def insert_feedback():
    feedback = request.form['feedback']
    # available_bikes = request.form['available_bikes']
    # send feedback to postgres here
    return redirect("/", code=302)


@app.route('/')
def index():
    number_station_index = 4006
    return render_template('prediction.html', list_stations=list_stations.values.tolist(),
                           number_station=number_station_index)
