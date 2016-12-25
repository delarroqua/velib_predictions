from velib_predictions.app.api_utils import get_station_individual, convert_timestamp
from datetime import timedelta
import pandas as pd


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
        temperature = 10
        humidity = 10
        wind = 10
        precipitation = 10

        array_to_predict = [number_station, weekday, hour, minute, latitude, longitude,
                            available_bikes_previous, weekday_previous, hour_previous, minute_previous,
                            temperature, humidity, wind, precipitation]
        prediction_array = model.predict([array_to_predict])
        prediction = int(prediction_array[0])
        return prediction
    #else:
    #   return 0



#if __name__ == '__main__':
#    from velib_predictions.utils.io import load_pickle
#    number_station = '4006'
#    model = load_pickle("files/model.pkl")
#    prediction = predict_available_bikes(model, number_station)
#    print("Prediction for station n°{0}: {1} available bikes".format(number_station, prediction))
