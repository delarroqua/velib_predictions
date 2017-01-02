from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.connection.data_loader import RawDataLoader

from velib_modules.model.model import RFTransformer
from velib_modules.model.evaluation import evaluate_model
from velib_modules.model.info import compute_model_information

from velib_modules.utils.io import load_json, paths_exist, export_pickle, load_pickle, load_dataframe_pickle, export_dataframe_pickle
from velib_modules.utils.df import SplitFeaturesTarget, FilterPostalCode
from velib_modules.utils.station_enricher import StationEnricherSimple

from sklearn.model_selection import train_test_split

import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



if __name__ == '__main__':

    # Set relevant lists
    postal_code_list = ['75004', '75011']
    columns_model_list = ['number', 'weekday', 'hour', 'minute', 'latitude', 'longitude', 'available_bikes_previous',
                          'weekday_previous', 'hour_previous', 'minute_previous']
    target_column = "available_bikes"

    # Create raw_data_loader
    config_db = load_json("config/config_db.json")
    connection = PostgresConnection(config_db)
    raw_data_loader = RawDataLoader(connection, cache_overwrite=False)

    # Load raw data
    config_query = load_json("config/config_query.json")
    stations_raw_df = raw_data_loader.load_table(config_query)

    # Filter df
    stations_filtered_df = FilterPostalCode(stations_raw_df, postal_code_list)


    if paths_exist("files/simple_model/features_train.pkl", "files/simple_model/features_test.pkl", "files/simple_model/target_train.pkl",
                   "files/simple_model/target_test.pkl"):
        logger.info("Retrieving features train and test from cache")
        features_train = load_dataframe_pickle("files/simple_model/features_train.pkl")
        features_test = load_dataframe_pickle("files/simple_model/features_test.pkl")
        target_train = load_dataframe_pickle("files/simple_model/target_train.pkl")
        target_test = load_dataframe_pickle("files/simple_model/target_test.pkl")
    else:
        # Enrich station
        logger.info("Enrich dataframe")
        start = time.time()
        station_enricher_simple = StationEnricherSimple(stations_df=stations_filtered_df)
        df_enriched = station_enricher_simple.enrich_stations()
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
        export_dataframe_pickle(features_train, "files/simple_model/features_train.pkl")
        export_dataframe_pickle(features_test, "files/simple_model/features_test.pkl")
        export_dataframe_pickle(target_train, "files/simple_model/target_train.pkl")
        export_dataframe_pickle(target_test, "files/simple_model/target_test.pkl")

    # Load model
    if paths_exist("files/simple_model/model.pkl"):
        logger.info("Loading cached model")
        model = load_pickle("files/simple_model/model.pkl")
    else:
        logger.info("Fitting model...")
        config_model = load_json("config/config_model.json")
        model = RFTransformer(config_model_parameters=config_model["random_forest_parameters"], columns=columns_model_list)
        model.fit(features_train, target_train)
        logger.info("Model fitted. Exporting...")
        export_pickle(model, "files/simple_model/model.pkl")

    logger.info("Uploading model information to database...")
    model_information = compute_model_information(model, features_train, features_test, target_test)
    connection.upload_model_information(model_information)

    logger.info("Evaluate model on validation set")
    model_performance = evaluate_model(model, features_test, target_test)
    print(model_performance)

    logger.info("Computing feature importance...")
    model.features_importance()
