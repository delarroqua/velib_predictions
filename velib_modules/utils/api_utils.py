from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.utils.io import load_json

import json
import requests
from datetime import datetime


config_velib = load_json("config/config_velib.json")
url = config_velib["url_api_velib"]["root"] + config_velib["url_api_velib"]["stations"]


def convert_timestamp(timestamp_to_convert):
    s = timestamp_to_convert / 1000.0
    return datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')

def get_weather_data():
    url_weather = "http://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url_weather, params=config_velib["openweathermap"])
    return json.loads(response.content.decode("utf8"))

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



def get_stations_list():
    response = requests.get(url, params=config_velib["params_api_velib"])
    return json.loads(response.content.decode("utf8"))


def get_station_individual(number_station):
    url_station = url + "/" + str(number_station)
    response = requests.get(url_station, params=config_velib["params_api_velib"])
    return json.loads(response.content.decode("utf8"))