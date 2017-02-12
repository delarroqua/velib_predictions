# Vélib' Prediction App

Predict availability of bikes stations in Paris.
You can find a series of article on these links
* [Part I: Data retrieval and storage in AWS] (https://medium.com/@pierredelarroqua/v%C3%A9lib-in-paris-part-i-discover-aws-and-postgresql-e0cf19d09988#.1fki9slsc)
* Part II: Web App with Flask that use a simple model in Python to predict availability of the stations
* Part III: Improving the model with additional features and a better algorithm


## Installation

#### Dependencies

* Python 3
* PostgreSQL
* Flask (http://flask.pocoo.org/)
* Requests (http://docs.python-requests.org/)
* db.py (https://github.com/yhat/db.py)

#### Create conda environment

```bash
conda create --name velib python=3.4
```

#### Switch to velib environment

```bash
source activate velib
```

#### Install python packages

```bash
python setup.py install
```

#### Train a Model

 ```bash
 python train_model.py
 ```
 
#### Run the application

 ```bash
 python run_server.py
 ```
 