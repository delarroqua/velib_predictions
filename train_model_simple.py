from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.connection.data_loader import RawDataLoader

from velib_modules.model.model import RFTransformer
from velib_modules.model.evaluation import evaluate_model
from velib_modules.model.info import compute_model_information

from velib_modules.utils.io import load_json, paths_exist, export_pickle, load_pickle, load_dataframe_pickle, export_dataframe_pickle
from velib_modules.utils.df import SplitFeaturesTarget, FilterPostalCode
from velib_modules.utils.station_enricher import enrich_stations_simple

from sklearn.model_selection import train_test_split

import os
import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Todo : Write a clean simple_model


if __name__ == '__main__':

    # Set out_directory
    out_directory = "files/simple_model/"

    # Set relevant lists
    postal_code_list = ['75004', '75011']
    columns_model_list = ['number', 'weekday', 'hour', 'minute', 'latitude', 'longitude', 'available_bikes_previous',
                          'weekday_previous', 'hour_previous', 'minute_previous']
    target_column = "available_bikes"


    # Load data
    if paths_exist(os.path.join(out_directory,"features_train.pkl"), os.path.join(out_directory,"features_test.pkl"),
                   os.path.join(out_directory,"target_train.pkl"), os.path.join(out_directory,"target_test.pkl")):
        logger.info("Retrieving features train and test from cache")
        features_train = load_dataframe_pickle(os.path.join(out_directory,"features_train.pkl"))
        features_test = load_dataframe_pickle(os.path.join(out_directory,"features_test.pkl"))
        target_train = load_dataframe_pickle(os.path.join(out_directory,"target_train.pkl"))
        target_test = load_dataframe_pickle(os.path.join(out_directory,"target_test.pkl"))
    else:
        # Create Connection
        config_db = load_json("config/config_db.json")
        connection = PostgresConnection(config_db)

        query = """ select * from {{table}} limit {{limit}} """
        config_query = {"table": "other.update_stations_with_previous_variables", "limit": 500000}
        stations_raw_df = connection.query(query, config_query)

        # Filter df
        stations_filtered_df = FilterPostalCode(stations_raw_df, postal_code_list)

        # Enrich station
        logger.info("Enrich dataframe")
        start = time.time()
        df_enriched = enrich_stations_simple(stations_filtered_df)
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

    # Load model
    if paths_exist(os.path.join(out_directory,"model.pkl")):
        logger.info("Loading cached model")
        model = load_pickle(os.path.join(out_directory,"model.pkl"))
    else:
        logger.info("Fitting model...")
        config_model = load_json("config/config_model.json")
        model = RFTransformer(config_model_parameters=config_model["random_forest_parameters"], columns=columns_model_list)
        model.fit(features_train, target_train)
        logger.info("Model fitted. Exporting...")
        export_pickle(model, os.path.join(out_directory,"model.pkl"))

    model_information = compute_model_information(model, features_train, features_test, target_test)
    logger.info("Uploading model information to database...")
    connection.upload_model_information(model_information)

    logger.info("Evaluate model on validation set")
    model_performance = evaluate_model(model, features_test, target_test)
    print(model_performance)

    logger.info("Computing feature importance...")
    model.features_importance()
