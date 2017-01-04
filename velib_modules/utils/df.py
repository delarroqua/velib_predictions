from sklearn.model_selection import train_test_split
from velib_modules.utils.io import paths_exist, export_dataframe_pickle, load_dataframe_pickle

import re

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def FilterWeatherData(df):
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered.temperature.notnull()]
    return df_filtered


def FilterPostalCode(df, postal_code_list):
    df_filtered = df.copy()
    df_filtered['postal_code'] = df_filtered.address.apply(lambda x: re.findall('\d{5}', x)[0])
    df_filtered = df_filtered[df_filtered.postal_code.isin(postal_code_list)]
    return df_filtered


def FilterPreviousVariables(df):
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered.available_bikes_previous.notnull()]
    return df_filtered


def SplitFeaturesTarget(df, target_column):
    target = df[target_column].astype(int)
    features = df.drop(target_column, 1)
    return features, target

