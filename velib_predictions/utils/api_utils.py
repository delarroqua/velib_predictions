from velib_predictions.connection.db_connection import PostgresConnection
from velib_predictions.utils.io import load_json

import pandas as pd
import json
import requests
from datetime import datetime, timedelta


config_velib = load_json("config/config_velib.json")


def get_weather_data():
    url_weather = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url_weather, params=config_velib["openweathermap"])
    return json.loads(response.content.decode("utf8"))


def get_station_individual(number_station):
    url_station = config_velib["url_api_velib"]["root"] + config_velib["url_api_velib"]["stations"] + "/" + str(number_station)
    response = requests.get(url_station, params=config_velib["params_api_velib"])
    return json.loads(response.content.decode("utf8"))


def convert_timestamp(timestamp_to_convert):
    s = timestamp_to_convert / 1000.0
    return datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')


def get_lat_long(number_station):
    config_db = load_json("config/config_db.json")
    connection = PostgresConnection(config_db)
    query = """
        SELECT latitude, longitude
        FROM api.stations_informations
        WHERE number = ({{ number_station }})::TEXT
        LIMIT 1
        """

    data = [
        {"number_station": number_station}
    ]

    df_lat_long = connection.query(query, data)
    latitude = float(df_lat_long['latitude'])
    longitude = float(df_lat_long['longitude'])
    return latitude, longitude


def predict_available_bikes(model, number_station):
    number_station = int(number_station)
    last_station_update = get_station_individual(number_station)

    if last_station_update != {'error': 'Station not found'}:
        # Get previous_date, available_bikes_previous, & lat-long
        previous_date = pd.to_datetime(convert_timestamp(last_station_update["last_update"]))
        available_bikes_previous = last_station_update["available_bike_stands"]
        latitude = last_station_update["position"]["lat"]
        longitude = last_station_update["position"]["lng"]

        # Previous date input
        weekday_previous = previous_date.weekday()
        hour_previous = previous_date.hour
        minute_previous = previous_date.minute

        # Evaluation date input
        evaluation_date = previous_date + timedelta(hours=1)
        weekday = evaluation_date.weekday()
        hour = evaluation_date.hour
        minute = evaluation_date.minute

        # weather data
        weather_data = get_weather_data()
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        precipitation = 1

        array_to_predict = [number_station, weekday, hour, minute, latitude, longitude,
                            available_bikes_previous, weekday_previous, hour_previous, minute_previous,
                            temperature, humidity, wind, precipitation]
        prediction_array = model.predict([array_to_predict])
        prediction = int(prediction_array[0])
        return prediction
    #else:
    #   return 0

