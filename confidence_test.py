from velib_modules.model.confidence import indice_confiance
from velib_modules.utils.io import load_dataframe_pickle, load_pickle
import os

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    out_directory = "files/classic_model/"
    features_test = load_dataframe_pickle(os.path.join(out_directory, "features_test.pkl"))
    print(features_test)
    target_test = load_dataframe_pickle(os.path.join(out_directory, "target_test.pkl"))
    model = load_pickle(os.path.join(out_directory, "model.pkl"))

    logger.info("Computing confidence indices")
    indice_confiance = indice_confiance(model, features_test, target_test, groupby_columns=['number'])
    print(indice_confiance)
    #indice_confiance.to_csv(out_directory, index=False)
