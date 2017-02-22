from velib_modules.utils.df import FilterPreviousVariables, FilterWeatherData

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def FilterTotalStands(df):
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered.bike_stands.notnull()]
    return df_filtered


def add_fill_rate(df):
    df_with_fill_rate = df.copy()
    df_with_fill_rate['fill_rate'] = (df.available_bikes / df.bike_stands).astype(float)
    df_with_fill_rate['fill_rate_previous'] = (df.available_bikes_previous / df.bike_stands).astype(float)
    return df_with_fill_rate


def add_date_variables(df):
    df_with_date_variables = df.copy()
    last_update = pd.to_datetime(df_with_date_variables.last_update)
    hour = last_update.dt.hour
    minute = last_update.dt.minute
    df_with_date_variables['weekday'] = last_update.dt.weekday
    df_with_date_variables['time_float'] = hour + minute / 60
    return df_with_date_variables


def add_previous_date_variables(df):
    df_with_previous = df.copy()
    last_update_previous = pd.to_datetime(df_with_previous.last_update_previous)
    hour_previous = last_update_previous.dt.hour
    minute_previous = last_update_previous.dt.minute
    df_with_previous['weekday_previous'] = last_update_previous.dt.weekday
    df_with_previous['time_float_previous'] = hour_previous + minute_previous / 60
    return df_with_previous


def add_weather_data(df, weather_data):
    df_copy = df.copy()
    df_copy['last_update_date'] = df_copy.last_update.apply(lambda x: x.date())
    df_with_weather = pd.merge(df_copy, weather_data, how='left', left_on='last_update_date', right_on='date')
    return df_with_weather


def load_weather_data(path_weather_data):
    weather_data_raw = pd.read_csv(path_weather_data)
    # Clean weather data
    weather_data = weather_data_raw[['CET', 'Mean TemperatureC', ' Mean Humidity', ' Mean Wind SpeedKm/h',
                                     'Precipitationmm']]  # ' CloudCover', ' Events'
    weather_data.columns = ['date', 'temperature', 'humidity', 'wind', 'precipitation']  # 'cloud', 'events'
    weather_data['date'] = pd.to_datetime(weather_data.date).apply(lambda x: x.date())
    return weather_data


def cast_df(df):
    df_casted = df.copy()
    # Convert number to int
    df_casted['number'] = df_casted.number.astype("int64")
    # Convert lat-long to float
    df_casted['latitude'] = df_casted.latitude.astype("float64")
    df_casted['longitude'] = df_casted.longitude.astype("float64")
    # Convert to float
    df_casted['available_bikes'] = df_casted.available_bikes.astype(float)
    df_casted['available_bikes_previous'] = df_casted.available_bikes_previous.astype(float)
    df_casted['bike_stands'] = df_casted.bike_stands.astype(float)
    return df_casted


def enrich_stations(df, columns_model_list):
    stations_df = df.copy()
    stations_df = FilterTotalStands(stations_df)
    stations_df = cast_df(stations_df)
    stations_df = add_date_variables(stations_df)
    stations_df = add_fill_rate(stations_df)

    # Load and add weather data
    # Get it at the following link : https://www.wunderground.com/history/airport/LFPB/2016/11/1/CustomHistory.html?dayend=3&monthend=2&yearend=2017&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1
    path_weather_data = 'files/input/paris_temperature.csv'
    weather_data = load_weather_data(path_weather_data)
    stations_df = add_weather_data(stations_df, weather_data)
    stations_df = FilterWeatherData(stations_df)  # Filter out rows without weather data

    stations_df = add_previous_date_variables(stations_df)
    stations_df = FilterPreviousVariables(stations_df)  # Filter out rows without previous variables

    stations_df_enriched = stations_df[columns_model_list+['fill_rate']]
    return stations_df_enriched
