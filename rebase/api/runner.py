import tempfile
import dill
import requests
import json
import pandas as pd
from datetime import datetime
import importlib
import rebase.util.api_request as api_request
import rebase as rb
# This class loads custom models created by the user

class ModelRunner():


    def __init__(self, model_id):
        self.model_id = model_id
        self.model_config = self.load_model_config()
        self.site_config = rb.Site.get(self.model_config['site_id'])
        self.model_class = self.load_pickle('code')()

        # need to add __builtins__ cuz of issue with Dill pickling it
        #self.model_class.get_weather.__globals__['__builtins__'] = importlib.import_module('builtins')



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
        weather_df = self.model_class.load_latest_data(self.site_config)
        # load the previously trained model
        model_trained = self.load_pickle('trained')
        pred_df = self.model_class.predict(model_trained, weather_df)
        print(pred_df)
        weather_df['forecast'] = pred_df
        pred_df = weather_df[['forecast']]
        pred_df = pred_df.div(self.site_config['capacity'][0]['value'])
        return pred_df


    def train(self, start_date, end_date):
        weather_df, observation_df = self.model_class.load_data(self.site_config, start_date, end_date)
        train_set = self.model_class.preprocess(weather_df, observation_df)

        model_trained, score = self.model_class.train(train_set, {})
        with tempfile.TemporaryDirectory() as tempdir:
            save_model_temp_as = '{}_{}'.format(tempdir, self.model_config['id'])
            upload_path = self.model_config['storage']['custom_model_trained_path']
            cs = CloudStorage(self.bucket)
            with open(save_model_temp_as, 'wb') as f:
                f.write(dill.dumps(model_trained))
                cs.upload_file(save_model_temp_as, upload_path)
