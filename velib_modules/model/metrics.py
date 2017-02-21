import numpy as np


def within_four(y_true, y_pred, threshold=4):
    return within_number(y_true, y_pred, threshold=threshold)


def within_three(y_true, y_pred, threshold=3):
    return within_number(y_true, y_pred, threshold=threshold)


def within_two(y_true, y_pred, threshold=2):
    return within_number(y_true, y_pred, threshold=threshold)


def within_number(y_true, y_pred, threshold):
    return np.mean(np.abs(y_true - y_pred) <= threshold)


def mean_percentage_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred) / (y_true + 1e-6))


def root_mean_squared_error(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean() ** 0.5


def mean_absolute_error(y_true, y_pred):
    return np.abs(y_true - y_pred).mean()
