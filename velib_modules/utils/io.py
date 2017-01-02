import json
import os
import pickle

import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def paths_exist(*args):
    return all(os.path.exists(path) for path in args)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def export_pickle(object, path):
    logger.info("exporting to %s", path)
    with open(path, 'wb') as f:
        pickle.dump(object, f, protocol=2) # protocol=2 to work with python 2.7


def load_pickle(path):
    logger.info("Loading from %s", path)
    with open(path, 'rb') as f:
        return pickle.load(f)


def export_dataframe(df, path):
    logger.info("exporting to %s", path)
    df.to_csv(path, index=False)


def load_dataframe(path):
    return pd.read_csv(path)


def export_dataframe_pickle(df, path):
    logger.info("exporting to %s", path)
    df.to_pickle(path)


def load_dataframe_pickle(path):
    logger.info("Loading from %s", path)
    return pd.read_pickle(path)

