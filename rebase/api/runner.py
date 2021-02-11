import tempfile
import dill
import requests
import json
import pandas as pd
from datetime import datetime
import importlib
import rebase as rb
import joblib

import rebase.util.api_request as api_request
# This class loads custom models created by the user

class ModelRunner():


    def __init__(self, model_id):
        self.model_id = model_id
        self.model_config = self.load_model_config()
        self.site_config = rb.Site.get(self.model_config['site_id'])
        self.model_class = self.load_pickle('code')()

        # need to add __builtins__ cuz of issue with Dill pickling it
        #self.model_class.get_weather.__globals__['__builtins__'] = importlib.import_module('builtins')
        self.model_class.load_data.__globals__['__builtins__'] = importlib.import_module('builtins')
        self.model_class.setup()


    def load_model_config(self):
        r = api_request.get('platform/v1/model/{}'.format(self.model_id))
        return r.json()


    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # !!! DANGER, loads arbitrary python code here !!!!
    # !!!    ONLY RUN IN AN ISOLATED ENVIRONMENT   !!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def load_pickle(self, file_type):
        r = api_request.get('platform/v1/model/custom/download/{}/{}'.format(file_type, self.model_id))
        return dill.loads(r.content)




    def predict(self, ref_time=None):
        ref_time = datetime.strptime(ref_time, '%Y/%m/%d/%H') if ref_time else ref_time
        weather_df, obs_df = self.model_class.load_latest_data(self.site_config)
        # load the previously trained model
        model_trained = self.load_pickle('trained')
        pred_set = self.model_class.preprocess(weather_df, observation_data=obs_df)
        pred_df = self.model_class.predict(model_trained, pred_set)
        weather_df['forecast'] = pred_df
        pred_df = weather_df[['forecast']]
        if 'capacity' in self.site_config and len(self.site_config['capacity'])>0:
            pred_df = pred_df.div(self.site_config['capacity'][-1]['value'])
        return pred_df

    def upload_single_forecast(self, ref_time, df_ref_time):
        to_iso = lambda d : d.strftime('%Y%m%dT%H:%M:%SZ')
        data = {
            'ref_time': to_iso(ref_time),
            'valid_time': [to_iso(d) for d in df_ref_time.index],
            'forecast': df_ref_time['forecast'].values.tolist()
        }

        path = 'platform/v1/model/custom/forecast/upload/{}'.format(self.model_id)
        r = api_request.post(path, data=json.dumps(data))
        if r.status_code != 200:
            raise Exception(f'Failed uploading forecast: model_id: {self.model_id}', r.status_code)

        return True

    def upload_forecast(self, df):
        ref_times = df.index.get_level_values('ref_datetime').unique()
        with joblib.parallel_backend("threading"):
            results = joblib.Parallel(n_jobs=4)(
                    joblib.delayed(self.upload_single_forecast)(ref_time, df.loc[(ref_time), :])
                           for ref_time in ref_times)

        if not all(results):
            raise Exception("There were some errors while uploading the forecasts, model_id: %s: %s" % (self.model_id, list(zip(ref_times, results))))


    def backtest(self):
        # load
        pass

    def hyperparam_search(self, params_search_space):
        
        pass


    def train(self, start_date, end_date, params={}):
        weather_df, observation_df = self.model_class.load_data(self.site_config, start_date, end_date)
        train_set = self.model_class.preprocess(weather_df, observation_data=observation_df)

        return self.model_class.train(train_set, params=params)

    def upload_trained_model(self, model_trained):
        path = 'platform/v1/model/custom/upload/trained/{}'.format(self.model_id)
        r = api_request.post(path, data=dill.dumps(model_trained))
        if r.status_code != 200:
            raise Exception('Failed uploading trained model', r.status_code)
