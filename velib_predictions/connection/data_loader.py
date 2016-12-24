from ..utils.io import paths_exist, export_dataframe_pickle, load_dataframe_pickle

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RawDataLoader:
    def __init__(self, connection, cache=True, cache_overwrite=False):
        self.connection = connection
        self.cache = cache
        self.cache_overwrite = cache_overwrite

    def load_table(self, config_query):
        table = config_query["table"]
        cache_path = "files/{table}.pkl".format(table=table)
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
        AND i.postal_code IN ('75004', '75011', '75012')
        limit {{limit}}
        """
        df = self.connection.query(query, config_query)
        return df
