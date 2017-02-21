from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestRegressor

from xgboost import XGBRegressor
import numpy as np

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTransformer(BaseEstimator):
    def __init__(self, config_model_parameters, columns):
        self.model_parameters = config_model_parameters
        self.model = None
        self.columns = columns
        self.model_training_time = 0
        self.name = None

    def fit(self, X_train, y_train):
        logger.info("Input shape %s", X_train.shape)
        logger.info("Training model %s ...", self.name)
        start = time.time()
        self.model.fit(X_train, y_train)
        self.model_training_time = time.time() - start
        model_training_time_minutes = int(self.model_training_time/60)
        logger.info("Training model took %s minutes", model_training_time_minutes)

    def predict(self, X):
        logger.info("Predict from model...")
        return self.model.predict(X)

    def features_importance(self, n=20):
        raise NotImplementedError("Feature importance method not implemented for this model")


class RFTransformer(ModelTransformer):
    def __init__(self, config_model_parameters, columns):
        super().__init__(config_model_parameters, columns)
        self.model = RandomForestRegressor(**self.model_parameters)
        self.name = "random forest"

    def features_importance(self, n=20):
        importance = self.model.feature_importances_
        logger.info("Feature importances :")
        for k, (i, f) in enumerate(reversed(sorted(zip(importance, self.columns)))):
            print(i, "->", f)
            if k == n:
                break


class XGBTransformer(ModelTransformer):
    def __init__(self, config_model_parameters, columns):
        super().__init__(config_model_parameters, columns)
        self.model = XGBRegressor(**self.model_parameters)
        self.name = "XGBoost"

    def features_importance(self, n=20):
        b = self.model.booster()
        fs = b.get_fscore()
        all_features = [fs.get(f, 0.) for f in b.feature_names]
        all_features = np.array(all_features, dtype=np.float32)
        importance = all_features / all_features.sum()
        logger.info("Feature importances")
        for k, (i, f) in enumerate(reversed(sorted(zip(importance, self.columns)))):
            logger.info("%s -> %f", f, i)
            if k == n:
                break