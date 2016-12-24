import pandas as pd

from datetime import timedelta

from velib_predictions.utils.df import FilterPreviousVariables, FilterWeatherData

class StationEnricher():
    def __init__(self, stations_df, weather_data):
        self.stations_df = stations_df
        self.weather_data = weather_data

    def add_weather_data(self, df):
        df_copy = df.copy()
        df_copy['last_update_date'] = df_copy.last_update_clean.apply(lambda x: x.date())
        df_with_weather = pd.merge(df_copy, self.weather_data, how='left', left_on='last_update_date', right_on='date')
        return df_with_weather


    def add_date_variables(self, df):
        df_with_date_variables = df.copy()
        df_with_date_variables['last_update_clean'] = pd.to_datetime(df_with_date_variables['last_update_clean'])
        df_with_date_variables['weekday'] = df_with_date_variables['last_update_clean'].dt.weekday
        df_with_date_variables['hour'] = df_with_date_variables['last_update_clean'].dt.hour
        df_with_date_variables['minute'] = df_with_date_variables['last_update_clean'].dt.minute
        return df_with_date_variables

    def find_previous_update(self, df_row):
        stations_df = self.stations_df
        number_station = df_row.number
        date_time = df_row.last_update_clean
        previous_date_time = date_time - timedelta(hours=1)
        dt_high = previous_date_time + timedelta(minutes=10)
        dt_low = previous_date_time - timedelta(minutes=10)
        previous_update_array = stations_df[(stations_df.number == number_station) \
                                            & (stations_df.last_update_clean < dt_high) \
                                            & (stations_df.last_update_clean > dt_low)]
        if (len(previous_update_array) != 0):
            previous_update = previous_update_array.iloc[0]
            last_update_previous = previous_update.last_update_clean
            available_bikes_previous = previous_update.available_bikes
        else:
            last_update_previous = None
            available_bikes_previous = None

        previous_update = pd.Series(
            {'last_update_previous': last_update_previous, 'available_bikes_previous': available_bikes_previous})
        return previous_update

    def add_previous_date_variables(self, df):
        previous_update = df.apply(self.find_previous_update, axis=1)
        df['last_update_previous'] = pd.to_datetime(previous_update['last_update_previous'])
        df['available_bikes_previous'] = previous_update['available_bikes_previous']

        df['weekday_previous'] = df.last_update_previous.dt.weekday
        df['hour_previous'] = df.last_update_previous.dt.hour
        df['minute_previous'] = df.last_update_previous.dt.minute
        return df

    def cast_df(self, df):
        df_casted = df.copy()
        # Convert number to int
        df_casted['number'] = df_casted.number.astype("int64")
        # Convert lat-long to float
        df_casted['latitude'] = df_casted.latitude.astype("float64")
        df_casted['longitude'] = df_casted.longitude.astype("float64")
        # Convert available_bikes_previous to int
        df_casted['available_bikes_previous'] = df_casted.available_bikes_previous.astype(int)
        return df_casted

    def enrich_stations(self):
        stations_df = self.stations_df.copy()
        stations_df = self.add_date_variables(stations_df)
        stations_df = self.add_weather_data(stations_df)
        stations_df = FilterWeatherData(stations_df)  # Filter out rows without weather data
        stations_df = self.add_previous_date_variables(stations_df)
        stations_df = FilterPreviousVariables(stations_df)  # Filter out rows without previous variables
        stations_df = self.cast_df(stations_df)
        stations_df_enriched = stations_df.drop(['last_update_clean', 'address', 'postal_code',
                                                 'last_update_previous', 'last_update_date', 'date'], 1)  # 'events'
        return stations_df_enriched
