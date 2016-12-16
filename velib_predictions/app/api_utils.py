from velib_predictions.connection.db_connection import PostgresConnection
from velib_predictions.utils.io import load_json

import json
import requests
from datetime import datetime


config_velib = load_json("config/config_velib.json")


def get_station_individual(number_station):
    url_station = config_velib["urls"]["root"] + config_velib["urls"]["stations"] + "/" + str(number_station)
    response = requests.get(url_station, params=config_velib["params"])
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