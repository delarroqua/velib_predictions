from velib_modules.model.metrics import root_mean_squared_error, within_two, mean_percentage_error, mean_absolute_error

def evaluate_model(model, features_test, y_test):
    y_pred = model.predict(features_test)
    performance = {}
    performance['RMSE'] = root_mean_squared_error(y_test, y_pred)
    performance['MAPE'] = mean_percentage_error(y_test, y_pred)
    performance['MAE'] = mean_absolute_error(y_test, y_pred)
    performance['within_two'] = within_two(y_test, y_pred)
    return performance
