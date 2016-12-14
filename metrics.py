import numpy as np


def within_error(y_true, y_pred, error=0.1):
    return np.mean(np.abs(y_true - y_pred) / (y_true + 1e-6) <= error)


def within_error_xgb(preds, dtrain, error=0.1):
    labels = dtrain.get_label()
    return 'WITHIN_0.1', within_error(labels, preds, error)


def within_two(y_true, y_pred, threshold=2):
    return np.mean(np.abs(y_true - y_pred) <= threshold)


def within_two_xgb(preds, dtrain, error=2):
    labels = dtrain.get_label()
    return 'WITHIN_2', within_two(labels, preds, error)


def root_mean_squared_error(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean() ** 0.5


def mean_absolute_error(y_true, y_pred):
    return np.abs(y_true - y_pred).mean()
