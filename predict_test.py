from velib_modules.api.predict import predict_available_bikes, predict_available_bikes_simple
from velib_modules.utils.io import load_pickle


if __name__ == '__main__':

    model_type = 'app'
    number_station = '4006'

    if (model_type == 'simple'):
        model = load_pickle("files/simple_model/model.pkl")
        prediction = predict_available_bikes_simple(model, number_station)
    else:
        model = load_pickle("files/app_model/model.pkl")
        prediction = predict_available_bikes_simple(model, number_station)

    if (prediction == 'error'):
        print('Error : no prediction available')
    else:
        print("Prediction for station n°{0}: {1} available bikes".format(number_station, prediction))