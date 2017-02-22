from velib_modules.api.predict import predict_available_bikes
from velib_modules.utils.io import load_pickle


if __name__ == '__main__':
    number_station = '4006'
    time_prediction = '1'
    path_model = "files/app_model/model.pkl"

    model = load_pickle(path_model)
    prediction = predict_available_bikes(model, number_station, time_prediction)

    if prediction == 'error':
        print('Error : no prediction available')
    else:
        print("Prediction for station n°{0}: {1} available bikes".format(number_station, prediction))
