from velib_predictions.connection.db_connection import PostgresConnection
from velib_predictions.connection.data_loader import RawDataLoader, load_weather_data

from velib_predictions.model.model import RFTransformer
from velib_predictions.model.evaluation import evaluate_model
from velib_predictions.model.info import compute_model_information

from velib_predictions.utils.io import load_json, paths_exist, export_pickle, load_pickle, load_dataframe_pickle
from velib_predictions.utils.df import get_features_and_targets, FilterPostalCode
from velib_predictions.utils.station_enricher import StationEnricher

import time
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Todo : Speedup function 'add_previous_date_variables' (enhancing using Cython ?)
# Todo : try to register to weather wunderground
# Todo : train a good model with the weather data
# Todo : test performance with weather data more rigourously

# Todo : Integrate cloud (remove Nan)
# Todo : Integrate events (create dummies)

# Todo : Essayer Keras sur les données



if __name__ == '__main__':

    # Set relevant lists
    postal_code_list = ['75004', '75011']
    # columns_model_list = ['number', 'weekday', 'hour', 'minute', 'latitude', 'longitude', 'available_bikes_previous',
    #                     'weekday_previous', 'hour_previous', 'minute_previous']
    columns_model_list = ['number', 'weekday', 'hour', 'minute', 'latitude', 'longitude', 'available_bikes_previous',
                          'weekday_previous', 'hour_previous', 'minute_previous',
                          'temperature', 'humidity', 'wind', 'precipitation'] # 'cloud', 'events'
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

    # Load weather data
    path_weather_data = 'paris_temperature.csv'
    weather_data = load_weather_data(path_weather_data)

    if paths_exist("files/features_train.pkl", "files/features_test.pkl", "files/target_train.pkl",
                   "files/target_test.pkl"):
        logger.info("Retrieving features train and test from cache")
        features_train = load_dataframe_pickle("files/features_train.pkl")
        features_test = load_dataframe_pickle("files/features_test.pkl")
        target_train = load_dataframe_pickle("files/target_train.pkl")
        target_test = load_dataframe_pickle("files/target_test.pkl")
    else:
        # Enrich station
        logger.info("Enrich dataframe")
        start = time.time()
        station_enricher = StationEnricher(stations_df=stations_filtered_df, weather_data=weather_data)
        df_enriched = station_enricher.enrich_stations()
        enricher_running_time = time.time() - start
        logger.info("Running enricher took %s", enricher_running_time)

        logger.info("Ratio data_enriched/data_raw : %s", len(df_enriched)/len(stations_raw_df))

        # Get features and target, divided by train & test
        features_train, features_test, target_train, target_test = get_features_and_targets(df_enriched, target_column)


    # Load model
    if paths_exist("files/model.pkl"):
        logger.info("Loading cached model")
        model = load_pickle("files/model.pkl")
    else:
        logger.info("Fitting model...")
        config_model = load_json("config/config_model.json")
        model = RFTransformer(config_model_parameters=config_model["random_forest_parameters"], columns=columns_model_list)
        model.fit(features_train, target_train)
        logger.info("Model fitted. Exporting...")
        export_pickle(model, "files/model.pkl")

    logger.info("Uploading model information to database...")
    model_information = compute_model_information(model, features_train, features_test, target_test)
    connection.upload_model_information(model_information)

    logger.info("Evaluate model on validation set")
    model_performance = evaluate_model(model, features_test, target_test)
    print(model_performance)

    logger.info("Computing feature importance...")
    model.features_importance()

    # print(model.predict(features_train[2:4].astype(int)))
    # print(features_train.info())
    # print(features_train.sample(n=1))
    # print(model.predict(features_train.sample(n=1)))
    # print(model.predict(np.array([2017, 48.86789, 2.34925, 3, 7, 26])))
    # print(model.predict([[2017, 48.86789, 2.34925, 3, 7, 26]]))


