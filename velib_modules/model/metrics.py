import numpy as np


def within_two(y_true, y_pred, threshold=2):
    return np.mean(np.abs(y_true - y_pred) <= threshold)

def mean_percentage_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred) / (y_true + 1e-6))

def root_mean_squared_error(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean() ** 0.5

def mean_absolute_error(y_true, y_pred):
    return np.abs(y_true - y_pred).mean()
