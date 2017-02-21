from velib_modules.utils.df import FilterPreviousVariables, FilterWeatherData

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def FilterTotalStands(df):
    df_filtered = df.copy()
    df_filtered = df_filtered[df_filtered.bike_stands.notnull()]
    return df_filtered

def add_fill_rate(df):
    df_with_fill_rate = df.copy()
    df_with_fill_rate['fill_rate'] = df.available_bikes / df.bike_stands
    df_with_fill_rate['fill_rate_previous'] = df.available_bikes_previous / df.bike_stands
    return df_with_fill_rate


def add_date_variables(df):
    df_with_date_variables = df.copy()
    df_with_date_variables['last_update'] = pd.to_datetime(df_with_date_variables.last_update)
    df_with_date_variables['weekday'] = df_with_date_variables.last_update.dt.weekday
    # df_with_date_variables['hour'] = df_with_date_variables.last_update.dt.hour
    # df_with_date_variables['minute'] = (df_with_date_variables.last_update.dt.minute/10).round(decimals=0)
    hour = df_with_date_variables.last_update.dt.hour
    minute = df_with_date_variables.last_update.dt.minute
    df_with_date_variables['time_float'] = hour + minute / 60
    return df_with_date_variables


def add_previous_date_variables(df):
    df_with_previous = df.copy()
    df_with_previous['last_update_previous'] = pd.to_datetime(df_with_previous.last_update_previous)
    df_with_previous['weekday_previous'] = df_with_previous.last_update_previous.dt.weekday
    # df_with_previous['hour_previous'] = df_with_previous.last_update_previous.dt.hour
    # df_with_previous['minute_previous'] = (df_with_previous.last_update_previous.dt.minute/10).round(decimals=0)
    hour_previous = df_with_previous.last_update_previous.dt.hour
    minute_previous = df_with_previous.last_update_previous.dt.minute
    df_with_previous['time_float_previous'] = hour_previous + minute_previous / 60
    return df_with_previous


def add_weather_data(df, weather_data):
    df_copy = df.copy()
    # df_copy.loc["last_update_date"] = df_copy.last_update_clean.apply(lambda x: x.date())
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
    # Convert to int
    df_casted['available_bikes'] = df_casted.available_bikes.astype(int)
    df_casted['available_bikes_previous'] = df_casted.available_bikes_previous.astype(float)
    df_casted['bike_stands'] = df_casted.bike_stands.astype(int)
    #df_casted['available_bikes_previous'] = df_casted.available_bikes_previous.astype(int)
    return df_casted


# Station Enricher Simple
def enrich_stations_simple(df):
    stations_df = df.copy()
    stations_df = add_date_variables(stations_df)
    stations_df = add_previous_date_variables(stations_df)
    stations_df = FilterPreviousVariables(stations_df)  # Filter out rows without previous variables
    stations_df = cast_df(stations_df)
    stations_df_enriched = stations_df.drop(['last_update', 'address', 'postal_code', 'last_update_previous'], 1)
    return stations_df_enriched


# Station Enricher Classic
def enrich_stations(df):
    stations_df = df.copy()
    stations_df = FilterTotalStands(stations_df)
    stations_df = cast_df(stations_df)
    stations_df = add_date_variables(stations_df)
    stations_df = add_fill_rate(stations_df)

    # Load and add weather data
    # Get it at the following link :
    path_weather_data = 'files/input/paris_temperature.csv'
    weather_data = load_weather_data(path_weather_data)
    stations_df = add_weather_data(stations_df, weather_data)
    stations_df = FilterWeatherData(stations_df)  # Filter out rows without weather data

    stations_df = add_previous_date_variables(stations_df)
    stations_df = FilterPreviousVariables(stations_df)  # Filter out rows without previous variables
    stations_df_enriched = stations_df.drop(['last_update', 'address', 'postal_code', 'last_update_previous',
                                             'last_update_date', 'date'], 1)
    return stations_df_enriched
