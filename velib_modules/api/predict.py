import pandas as pd
from datetime import timedelta

from velib_modules.utils.api_utils import convert_timestamp, get_station_individual


def predict_available_bikes_simple(model, number_station):
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

        array_to_predict = [number_station, weekday, hour, minute, latitude, longitude,
                            available_bikes_previous, weekday_previous, hour_previous, minute_previous]


        try:
            prediction = int(model.predict([array_to_predict])[0])
        except KeyError:
            prediction = 'error'

    return prediction