from velib_modules.api.predict import predict_available_bikes
from velib_modules.utils.io import load_pickle

if __name__ == '__main__':
    number_station = '4006'
    model = load_pickle("files/model.pkl")
    prediction = predict_available_bikes(model, number_station)
    print("Prediction for station n°{0}: {1} available bikes".format(number_station, prediction))