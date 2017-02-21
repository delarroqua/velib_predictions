from setuptools import setup, find_packages

setup(name='velib-prediction',
      description='Vélib - availability prediction',
      version='0.1',
      install_requires=['scipy', 'numpy', 'pandas==0.19.1', 'scikit-learn==0.18.1', 'db.py==0.5.2',
                        'psycopg2', 'flask==0.11.1', 'Jinja2==2.8', 'requests==2.9.1', 'xgboost==0.6a2'],
      packages=find_packages(),
     )