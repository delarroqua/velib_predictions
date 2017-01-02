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


def get_features_and_targets(df, target_column):
    if paths_exist("files/features_train.pkl", "files/features_test.pkl", "files/target_train.pkl",
                   "files/target_test.pkl"):
        logger.info("Retrieving features train and test from cache")
        features_train = load_dataframe_pickle("files/features_train.pkl")
        features_test = load_dataframe_pickle("files/features_test.pkl")
        target_train = load_dataframe_pickle("files/target_train.pkl")
        target_test = load_dataframe_pickle("files/target_test.pkl")
    else:
        logger.info("Split target and features")
        features, target = SplitFeaturesTarget(df, target_column)
        logger.info("Train/test split")
        features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.2,
                                                                                    random_state=42)
        logger.info("Exporting splitted dataset...")
        export_dataframe_pickle(features_train, "files/features_train.pkl")
        export_dataframe_pickle(features_test, "files/features_test.pkl")
        export_dataframe_pickle(target_train, "files/target_train.pkl")
        export_dataframe_pickle(target_test, "files/target_test.pkl")
    return features_train, features_test, target_train, target_test