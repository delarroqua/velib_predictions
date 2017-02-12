from velib_modules.model.metrics import mean_percentage_error
import pandas as pd

def indice_confiance(model, features_test, target_test, groupby_columns):
    df = features_test.copy()
    df['prediction'] = model.predict(features_test)
    df['target'] = target_test
    df = df[groupby_columns+['prediction', 'target']]
    def aggregate_MAPE(group):
        return pd.Series([mean_percentage_error(group.target, group.prediction), group.shape[0]],
                         index=['mape', 'n_obs'])

    mape_grouped = df.groupby(groupby_columns).apply(aggregate_MAPE).reset_index()
    qbins = pd.qcut(mape_grouped.mape, [0, 0.05, 0.25, 0.5, 0.75, 0.95, 1],
                    labels=range(0, 6)).astype(int)
    mape_grouped['confiance'] = 7 - qbins
    mape_grouped.loc[mape_grouped.n_obs < 100, 'confiance'] = mape_grouped.confiance - 2
    mape_grouped.loc[mape_grouped.confiance < 1, 'confiance'] = 1
    return mape_grouped
