import pandas as pd
import re
from datetime import timedelta

from velib_modules.utils.api_utils import convert_timestamp, get_station_individual,\
    get_weather_data_owm, get_weather_data_wg


def predict_available_bikes(model, number_station, time_prediction):
    number_station = int(number_station)
    last_station_update = get_station_individual(number_station)

    if last_station_update != {'error': 'Station not found'}:
        # Get previous_date, available_bikes_previous, lat-long, & total bike_stands
        previous_date = pd.to_datetime(convert_timestamp(last_station_update["last_update"]))
        available_bikes_previous = last_station_update["available_bike_stands"]
        latitude = last_station_update["position"]["lat"]
        longitude = last_station_update["position"]["lng"]
        bike_stands = last_station_update["bike_stands"]

        # Previous date input
        weekday_previous = previous_date.weekday()
        hour_previous = previous_date.hour
        minute_previous = previous_date.minute
        time_float_previous = hour_previous + minute_previous / 60
        fill_rate_previous = available_bikes_previous / bike_stands

        # Evaluation date input
        evaluation_date = previous_date + timedelta(hours=int(time_prediction))
        weekday = evaluation_date.weekday()
        hour = evaluation_date.hour
        minute = evaluation_date.minute
        time_float = hour + minute / 60

        # weather data (open weather map)
        # weather_data = get_weather_data_owm()
        # temperature = weather_data['main']['temp']
        # humidity = weather_data['main']['humidity']
        # wind = weather_data['wind']['speed']
        # precipitation = 0

        # weather data (wunderground)
        weather_data = get_weather_data_wg()
        temperature = weather_data['current_observation']['temp_c']
        humidity_raw = weather_data['current_observation']['relative_humidity']
        humidity = re.findall(r'\d+', humidity_raw)[0]
        wind = weather_data['current_observation']['wind_kph']
        precipitation = weather_data['current_observation']['precip_today_in']

        df_to_predict = pd.DataFrame({
            'number': [number_station],
            'latitude': [float(latitude)],
            'longitude': [float(longitude)],
            'weekday': [weekday],
            'time_float': [time_float],
            'bike_stands': [bike_stands],
            'weekday_previous': [weekday_previous],
            'time_float_previous': [time_float_previous],
            'fill_rate_previous': [fill_rate_previous],
            'temperature': [temperature],
            'humidity': [float(humidity)],
            'wind': [wind],
            'precipitation': [float(precipitation)]
        })

        prediction_array = model.predict(df_to_predict)
        fill_rate = float(prediction_array[0])
        available_bikes = int(fill_rate * bike_stands)
        return available_bikes, bike_stands
