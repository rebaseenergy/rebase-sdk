import rebase.util.api_request as api_request
import pandas as pd
import json
import pickle

def get_cached_weather(cache_file):
    try:
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    except:
        return None

def save_cached_weather(cache_file, df):
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump(df, f)
    except:
        pass


def json_to_df(json_data):
    df = pd.read_json(json_data)
    df.index = pd.MultiIndex.from_arrays(
             [pd.to_datetime(df['ref_datetime'].values),
             pd.to_datetime(df['valid_datetime'].values)],
             names=['ref_datetime', 'valid_datetime'])
    # Drop now duplicated index columns
    df = df.drop(columns=['ref_datetime', 'valid_datetime'])
    return df


def resample(df, resolution):
    return df.reset_index() \
                .set_index(df.index.get_level_values(1)) \
                .groupby(df.index.get_level_values(0)) \
                .resample(resolution).mean().interpolate(method='linear')

class Weather():

    @classmethod
    def historical(cls, params, resolution=None):
        path = '/weather/v1/get_nwp'
        json_params = json.dumps(params)
        cache_file = 'cache/{}.pickle'.format(json_params)

        df = get_cached_weather(cache_file)
        if df is None:
            response = api_request.get(path, params={'query_params': json_params})
            if response.status_code != 200:
                raise Exception('Failed retrieving weather data, status: {}'.format(response.status_code))
            df = json_to_df(response.text)

        save_cached_weather(cache_file, df)

        if resolution:
            df = resample(df, resolution)

        return df
