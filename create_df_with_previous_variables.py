from velib_modules.connection.db_connection import PostgresConnection
from velib_modules.utils.io import load_json
from velib_modules.utils.df import FilterPostalCode, AddPostalCode

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
    out_directory = "files/app_model/"
    #postal_code_list = ['75001', '75002', '75003', '75004', '75005', '75006', '75007', '75008', '75009', '75010',
    #                    '75011', '75012', '75013', '75014', '75015', '75016', '75017', '75018', '75019', '75020']
    postal_code_list = 0

    # Create Connection
    config_db = load_json("config/config_db.json")
    connection = PostgresConnection(config_db)

    query = """
           select *
           from {{table}}
           limit {{limit}}
           """

    config_query = {"table": "other.update_stations_clean", "limit": 5000000}

    logger.info("Extract stations_raw_df")
    stations_raw_df = connection.query(query, config_query)

    if (postal_code_list != 0):
        # Add Postal Code
        logger.info("Add postal code")
        df_with_postal_code = AddPostalCode(stations_raw_df)
        # Filter df
        stations_filtered_df = FilterPostalCode(df_with_postal_code, postal_code_list)
    else:
        stations_filtered_df = stations_raw_df

    add_previous_variables = AddPreviousVariables(stations_filtered_df)
    logger.info("Add previous variables")
    start = time.time()
    previous_update = stations_filtered_df.apply(add_previous_variables.find_previous_update, axis=1)
    running_time = time.time() - start
    logger.info("Adding %s variables took %s", len(stations_filtered_df.index), running_time)

    stations_filtered_df['last_update_previous'] = pd.to_datetime(previous_update['last_update_previous'])
    stations_filtered_df['available_bikes_previous'] = (previous_update['available_bikes_previous']).astype(float)

    #print(df[df.available_bikes_previous > 10])

    stations_filtered_df.to_csv("df_with_previous_variables.csv")  # header=False






