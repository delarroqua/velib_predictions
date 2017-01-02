from velib_predictions.model.evaluation import evaluate_model


def compute_model_information(model, features_train, features_test, target_test):
    model_information = {}
    model_information['train_size'] = features_train.shape[0]
    model_information['train_columns'] = list(features_train.columns)
    model_information['test_size'] = features_test.shape[0]
    model_information['features_names'] = model.columns
    model_information['model_name'] = model.name
    model_information['model_config'] = model.model_parameters
    model_information['model_training_time'] = model.model_training_time
    model_information['model_performance'] = evaluate_model(model, features_test, target_test)
    return model_information


