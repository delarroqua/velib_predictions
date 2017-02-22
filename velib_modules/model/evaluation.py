from velib_modules.model.metrics import root_mean_squared_error, mean_percentage_error, mean_absolute_error, \
                                        within_two, within_three, within_four


def evaluate_model(model, features_test, y_test):
    y_pred = model.predict(features_test)
    bikes_pred = (y_pred * features_test.bike_stands).astype(int)
    bikes_actual = (y_test * features_test.bike_stands).astype(int)
    performance = {}
    performance['RMSE'] = root_mean_squared_error(bikes_actual, bikes_pred)
    performance['MAPE'] = mean_percentage_error(bikes_actual, bikes_pred)
    performance['MAE'] = mean_absolute_error(bikes_actual, bikes_pred)
    performance['within_two'] = within_two(bikes_actual, bikes_pred)
    performance['within_three'] = within_three(bikes_actual, bikes_pred)
    performance['within_four'] = within_four(bikes_actual, bikes_pred)
    return performance
