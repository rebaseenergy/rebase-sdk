import tempfile
import dill
import requests
import json
import pandas as pd
from datetime import datetime
import importlib
import rebase as rb

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
        pred_df = pred_df.div(self.site_config['capacity'][0]['value'])
        return pred_df


    def upload_forecast(self, df):
        path = 'platform/v1/model/custom/forecast/upload/{}'.format(self.model_id)
        ref_time = df.index[0][0].strftime('%Y-%m-%d %H:%M')
        df = df.loc[ref_time].reset_index()
        data = {
            'ref_time': ref_time,
            'valid_time': df['valid_datetime'].values.tolist(),
            'forecast': df['forecast'].values.tolist(),
        }
        r = api_request.post(path, data=json.dumps(data))
        if r.status_code != 200:
            raise Exception('Failed uploading forecast', r.status_code)


    def backtest(self):
        # load
        pass


    def train(self, start_date, end_date):
        weather_df, observation_df = self.model_class.load_data(self.site_config, start_date, end_date)
        train_set = self.model_class.preprocess(weather_df, observation_data=observation_df)

        return self.model_class.train(train_set, {})

    def upload_trained_model(self, model_trained):
        path = 'platform/v1/model/custom/upload/trained/{}'.format(self.model_id)
        r = api_request.post(path, data=dill.dumps(model_trained))
        if r.status_code != 200:
            raise Exception('Failed uploading trained model', r.status_code)
