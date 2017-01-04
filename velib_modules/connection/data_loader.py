from velib_modules.utils.df import SplitFeaturesTarget, FilterPostalCode
from velib_modules.utils.station_enricher import enrich_stations_simple, enrich_stations

from velib_modules.utils.io import paths_exist, export_dataframe_pickle, load_dataframe_pickle

from sklearn.model_selection import train_test_split

import os
import time
import pandas as pd

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_features_and_targets(target_column, postal_code_list, connection, config_query, out_directory, type_enricher, weather_data):
    # Load data
    if paths_exist(os.path.join(out_directory,"features_train.pkl"), os.path.join(out_directory,"features_test.pkl"),
                   os.path.join(out_directory,"target_train.pkl"), os.path.join(out_directory,"target_test.pkl")):
        logger.info("Retrieving features train and test from cache")
        features_train = load_dataframe_pickle(os.path.join(out_directory,"features_train.pkl"))
        features_test = load_dataframe_pickle(os.path.join(out_directory,"features_test.pkl"))
        target_train = load_dataframe_pickle(os.path.join(out_directory,"target_train.pkl"))
        target_test = load_dataframe_pickle(os.path.join(out_directory,"target_test.pkl"))
    else:
        query = """ select {{columns}} from {{table}} limit {{limit}} """
        stations_raw_df = connection.query(query, config_query)

        # Filter df
        stations_filtered_df = FilterPostalCode(stations_raw_df, postal_code_list)

        # Enrich station
        logger.info("Enrich dataframe")
        start = time.time()

        if (type_enricher == 'simple'):
            df_enriched = enrich_stations_simple(stations_filtered_df)
        else:
            df_enriched = enrich_stations(stations_filtered_df, weather_data)

        enricher_running_time = time.time() - start
        logger.info("Running enricher took %s", enricher_running_time)

        logger.info("Ratio data_enriched/data_raw : %s", len(df_enriched)/len(stations_raw_df))

        # Get features and target, divided by train & test
        logger.info("Split target and features")
        features, target = SplitFeaturesTarget(df_enriched, target_column)
        logger.info("Train/test split")
        features_train, features_test, target_train, target_test = \
            train_test_split(features, target, test_size=0.2, random_state=42)

        logger.info("Exporting splitted dataset...")
        export_dataframe_pickle(features_train, os.path.join(out_directory,"features_train.pkl"))
        export_dataframe_pickle(features_test, os.path.join(out_directory,"features_test.pkl"))
        export_dataframe_pickle(target_train, os.path.join(out_directory,"target_train.pkl"))
        export_dataframe_pickle(target_test, os.path.join(out_directory,"target_test.pkl"))
    return features_train, features_test, target_train, target_test


def load_weather_data(path_weather_data):
    weather_data_raw = pd.read_csv(path_weather_data)
    # Clean weather data
    weather_data = weather_data_raw[['CET', 'Mean TemperatureC', ' Min Humidity', ' Mean Wind SpeedKm/h',
                                     'Precipitationmm']]  # ' CloudCover', ' Events'
    weather_data.columns = ['date', 'temperature', 'humidity', 'wind', 'precipitation']  # 'cloud', 'events'
    weather_data['date'] = pd.to_datetime(weather_data.date).apply(lambda x: x.date())
    return weather_data



class RawDataLoader:
    def __init__(self, connection, cache=True, cache_overwrite=False):
        self.connection = connection
        self.cache = cache
        self.cache_overwrite = cache_overwrite

    def load_table(self, config_query):
        table = config_query["table"]
        cache_path = "files/simple_model/{table}.pkl".format(table=table)
        if self.cache:
            if paths_exist(cache_path):
                if self.cache_overwrite:
                    logger.info("Retrieving from database")
                    df = self.load_table_sql_stations(config_query)
                    export_dataframe_pickle(df, cache_path)
                else:
                    logger.info("Retrieving from cache")
                    df = load_dataframe_pickle(cache_path)
            else:
                logger.info("Retrieving from database")
                df = self.load_table_sql_stations(config_query)
                export_dataframe_pickle(df, cache_path)
        else:
            df = self.load_table_sql_stations(config_query)
        return df

    def load_table_sql_stations(self, config_query):
        """
        Load data from a table specified in the config_query dictionary and returns a pandas dataframe
        :param config_query: dictionary containing the following keys: "table" (string),
        "columns" (array), and "limit" (integer)
        :return: pandas dataframe containing the requested table
        """
        query = """
        WITH A AS (
        select
         (response_api -> 'number')::TEXT        AS number,
         (response_api -> 'address')::TEXT       AS address,
         (response_api -> 'position' -> 'lat')::TEXT       AS latitude,
         (response_api -> 'position' -> 'lng')::TEXT       AS longitude,
          response_api -> 'available_bikes'      AS available_bikes,
        ((response_api -> 'last_update_clean')::TEXT)::TIMESTAMP     AS last_update_clean
        from {{table}}
        )
        SELECT A.*
        FROM other.stations_informations_enhanced i, A
        WHERE i.number = A.number
        AND i.postal_code IN ('75004', '75011')
        limit {{limit}}
        """
        df = self.connection.query(query, config_query)
        return df
