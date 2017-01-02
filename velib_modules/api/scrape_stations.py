from velib_modules.utils.io import load_json
from velib_modules.utils.api_utils import convert_timestamp, get_stations_list

import json
import psycopg2
from datetime import datetime


config_db = load_json("config/config_db.json")

conn = None
conn = psycopg2.connect(database=config_db['db'], user=config_db['user'], host=config_db['host'], password=config_db['password'])
cur = conn.cursor()


def scrape_stations():
    stations_list = get_stations_list()

    for result in stations_list:
        result["last_update_clean"] = convert_timestamp(result["last_update"])
        query = "INSERT INTO api.update_stations (datetime, response_api) VALUES (%s, %s)"
        cur.execute(query, (datetime.now(), json.dumps(result)))
        conn.commit()


