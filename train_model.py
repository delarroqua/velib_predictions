from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.connection.data_loader import get_features_and_targets, load_weather_data

from velib_modules.model.model import RFTransformer
from velib_modules.model.evaluation import evaluate_model
from velib_modules.model.info import compute_model_information

from velib_modules.utils.io import load_json, paths_exist, export_pickle, load_pickle

import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Todo : Speedup function 'add_previous_date_variables' (enhancing using Cython ?)

# Todo : Integrate cloud (remove Nan)
# Todo : Integrate events (create dummies)
# Todo : Essayer Keras sur les données



if __name__ == '__main__':

    # Set variables
    type_enricher = "classic"
    out_directory = "files/classic_model/"
    postal_code_list = ['75004', '75011']
    target_column = "available_bikes"

    # Create raw_data_loader
    config_db = load_json("config/config_db.json")
    connection = PostgresConnection(config_db)

    # Load config query
    config_query = load_json("config/config_query.json")

    # Load data
    features_train, features_test, target_train, target_test = \
        get_features_and_targets(target_column, postal_code_list, connection, config_query, out_directory,
                                 type_enricher)

    # Set features of model
    columns_model_list = ['number', 'weekday', 'hour', 'minute', 'latitude', 'longitude', 'available_bikes_previous',
                          'weekday_previous', 'hour_previous', 'minute_previous',
                          'temperature', 'humidity', 'wind', 'precipitation']  # 'cloud', 'events'

    # Load model
    if paths_exist(os.path.join(out_directory, "model.pkl")):
        logger.info("Loading cached model")
        model = load_pickle(os.path.join(out_directory, "model.pkl"))
    else:
        logger.info("Fitting model...")
        config_model = load_json("config/config_model.json")
        model = RFTransformer(config_model_parameters=config_model["random_forest_parameters"],
                              columns=columns_model_list)
        model.fit(features_train, target_train)
        logger.info("Model fitted. Exporting...")
        export_pickle(model, os.path.join(out_directory, "model.pkl"))

    model_information = compute_model_information(model, features_train, features_test, target_test)
    logger.info("Uploading model information to database...")
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


