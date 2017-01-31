from velib_modules.utils.df import SplitFeaturesTarget, FilterPostalCode, AddPostalCode
from velib_modules.utils.station_enricher import enrich_stations_simple # enrich_stations

from velib_modules.utils.io import paths_exist, export_dataframe_pickle, load_dataframe_pickle

from sklearn.model_selection import train_test_split

import os
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_features_and_targets(target_column, postal_code_list, connection, config_query, out_directory, type_enricher):
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

        # Add Postal Code
        logger.info("Add postal code")
        df_with_postal_code = AddPostalCode(stations_raw_df)

        # Filter df
        if (postal_code_list != 0):
            stations_filtered_df = FilterPostalCode(df_with_postal_code, postal_code_list)
        else:
            stations_filtered_df = df_with_postal_code

        # Enrich station
        logger.info("Enrich dataframe")
        start = time.time()

        if (type_enricher == "simple"):
            df_enriched = enrich_stations_simple(stations_filtered_df)
        elif (type_enricher == "classic"):
            df_enriched = enrich_stations(stations_filtered_df)
        else:
            logger.info("Wrong type of enricher")

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
