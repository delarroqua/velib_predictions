from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.utils.io import load_json

import pandas as pd
import numpy as np
from datetime import timedelta
import time

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddPreviousVariables():
    def __init__(self, stations_df):
        self.stations_df = stations_df

    def find_previous_update(self, df_row):
        stations_df = self.stations_df
        number_station = df_row.number
        date_time = df_row.last_update
        previous_date_time = date_time - timedelta(hours=1)
        dt_high = previous_date_time + timedelta(minutes=10)
        dt_low = previous_date_time - timedelta(minutes=10)
        previous_update_array = stations_df[(stations_df.number == number_station) \
                                            & (stations_df.last_update < dt_high) \
                                            & (stations_df.last_update > dt_low)]
        if (len(previous_update_array) != 0):
            previous_update = previous_update_array.iloc[0]
            last_update_previous = previous_update.last_update
            available_bikes_previous = previous_update.available_bikes
        else:
            last_update_previous = np.nan
            available_bikes_previous = np.nan

        previous_update = pd.Series(
            {'last_update_previous': last_update_previous, 'available_bikes_previous': available_bikes_previous})
        return previous_update


if __name__ == '__main__':

    # Set out_directory
    out_directory = "files/simple_model/"

    # Create Connection
    config_db = load_json("config/config_db.json")
    connection = PostgresConnection(config_db)

    query = """
           select
            (response_api -> 'number')::TEXT        AS number,
            (response_api -> 'address')::TEXT       AS address,
            (response_api -> 'position' -> 'lat')::TEXT       AS latitude,
            (response_api -> 'position' -> 'lng')::TEXT       AS longitude,
             response_api -> 'available_bikes'      AS available_bikes,
           ((response_api -> 'last_update_clean')::TEXT)::TIMESTAMP     AS last_update
           from {{table}}
           limit {{limit}}
           """

    config_query = {"table": "api.update_stations", "limit": 2000000}

    df = connection.query(query, config_query)

    add_previous_variables = AddPreviousVariables(df)
    logger.info("Add previous variables")
    start = time.time()
    previous_update = df.apply(add_previous_variables.find_previous_update, axis=1)
    running_time = time.time() - start
    logger.info("Adding variables took %s", running_time)

    df['last_update_previous'] = pd.to_datetime(previous_update['last_update_previous'])
    df['available_bikes_previous'] = (previous_update['available_bikes_previous']).astype(float)

    #print(df[df.available_bikes_previous > 10])

    df.to_csv("df_with_previous_variables.csv")  # header=False






