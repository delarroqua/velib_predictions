# Vélib' Prediction App

Predict availability of bikes stations in Paris.
You can find a series a article on these link
* [Part I: Data retrieval and storage in AWS] (https://medium.com/@pierredelarroqua/v%C3%A9lib-in-paris-part-i-discover-aws-and-postgresql-e0cf19d09988#.1fki9slsc)
* Part II: Web App with Flask that use a simple model in Python to predict availability of the stations
* Part III: Improving the model with additional features and a better algorithm

## Dependencies

* Python 3
* PostgreSQL
* Flask (http://flask.pocoo.org/)
* Requests (http://docs.python-requests.org/)
* db.py (https://github.com/yhat/db.py)

## Training a Model

 ```bash
 python train_model.py
 ```