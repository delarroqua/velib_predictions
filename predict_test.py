from velib_modules.api.predict import predict_available_bikes
from velib_modules.utils.io import load_pickle

import os


if __name__ == '__main__':
    number_station = '4006'
    time_prediction = '1'

    path_model = "files/app_model/"
    # knn = load_pickle(os.path.join(path_model, 'knn.pkl'))
    model = load_pickle(os.path.join(path_model, 'model.pkl'))

    # Get prediction from model
    available_bikes, bike_stands = predict_available_bikes(model, number_station, time_prediction)  # knn

    if available_bikes is None:
        print('Error : no prediction available')
    else:
        print("Prediction for station n°{0}: {1} available bikes sur {2} bike stands".format(number_station,
                                                                                             available_bikes,
                                                                                             bike_stands))
