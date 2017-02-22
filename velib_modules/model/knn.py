from sklearn.base import TransformerMixin
from sklearn.neighbors import KNeighborsRegressor
import numpy as np


class KnnModel(TransformerMixin):
    def __init__(self, k=10):
        self.k = k
        self.knn = KNeighborsRegressor(n_neighbors=self.k, weights='uniform', metric='minkowski')

    def add_knn_feature(self, df):
        df['knn'] = self.predict(df)
        return df

    def fit(self, df, y):
        X = np.array(df[['latitude', 'longitude']])
        self.knn.fit(X, y)
        return self

    def predict(self, df):
        X = np.array(df[['latitude', 'longitude']])
        return self.knn.predict(X)
