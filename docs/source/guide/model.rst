Creating a custom model
=======================

Define your model class
-----------------------

Your custom model class must implement a specific interface to be able to communicate with the platform.

It must:

1. extend the :class:`rebase.Model` base class
2. implement :meth:`rebase.Model.load_data` method
3. implement :meth:`rebase.Model.load_latest_data` method
4. implement :meth:`rebase.Model.preprocess` method
5. implement :meth:`rebase.Model.train` method
6. implement :meth:`rebase.Model.predict` method

You are free to create any other **helper methods** within the class

Here is a full example:

::

  import rebase as rb
  import lightgbm as lgb
  import numpy as np
  import pandas as pd

  class MyModel(rb.Model):


    def load_data(self, site_config, start_date, end_date):
        lat, lon = site_config['latitude'], site_config['longitude']
        observation_df = rb.Site.observation(site_config['site_id'], start_date, end_date)
        params = {
            'model': 'DWD_ICON-EU',
            'start_date': pd.to_datetime(start_date).strftime("%Y-%m-%d %H"),
            'end_date': pd.to_datetime(end_date).strftime("%Y-%m-%d %H"),
            'coords': {'latitude': [lat], 'longitude': [lon]},
            'variables': ['Temperature', 'CloudCover'],
            'as_dataframe': True
        }

        weather_df = rb.Weather.historical(params, resolution='15T')
        return weather_df, observation_df


    def load_latest_data(self, site_config):
        lat, lon = site_config['latitude'], site_config['longitude']
        params = {
            'model': 'DWD_ICON-EU',
            'coords': {'latitude': [lat], 'longitude': [lon]},
            'variables': ['Temperature', 'CloudCover'],
            'as_dataframe': True
        }

        weather_df = rb.Weather.operational(params, resolution='15T')
        return weather_df, None


    def preprocess(self, weather_data, observation_data=None):
        if observation_data is not None:
            obs_intep = observation_data.reindex(index=weather_data.index.get_level_values("valid_datetime")) \
                            .interpolate() \
                            .set_index(weather_data.index)

            df = weather_data.join(obs_intep, how='inner')
        else:
            df = weather_data

        # time related features
        timestamps = df.index.get_level_values('valid_datetime')
        seconds_in_day = 24*60*60
        df.loc[:, 'sin_time_hd'] = np.sin(2*np.pi*(timestamps-timestamps.round("D")).total_seconds()/seconds_in_day)
        df.loc[:, 'cos_time_hd'] = np.cos(2*np.pi*(timestamps-timestamps.round("D")).total_seconds()/seconds_in_day)
        df.loc[:, 'time_hod'] = timestamps.hour
        df.loc[:, 'dow'] = timestamps.dayofweek
        df.loc[:, 'cal_weekday'] = timestamps.dayofweek.isin([0, 1, 2, 3, 4]).astype('int')
        df.loc[:, 'cal_weekend'] = timestamps.dayofweek.isin([5, 6]).astype('int')

        if observation_data is not None:
            df_X = df.drop(columns=['observation'])
            df_y = df['observation']
        else:
            df_X = df.copy()
            df_y = None

        dataset = lgb.Dataset(df_X, label=df_y, params={'verbose': -1}, free_raw_data=False)

        return dataset

    def train(self, train_set, params={}):

        valid_sets = [train_set]
        valid_names = ['train']

        evals_result = {}
        params['objective'] = 'quantile'
        params['alpha'] = 0.5
        gbm = lgb.train({"learning_rate": 0.1,
                              "num_trees": 500,
                              "boosting": "gbdt",
                              "max_leaves": 64,
                              "max_depth": 8,
                              "min_data_in_leaf": 10,
                              "max_bin": 255,
                              "bagging_fraction": 0.5,
                              "bagging_freq": 5,
                              "feature_fraction": 1.0,
                              "early_stopping": 20,
                              "lambda_l1": 0.0,
                              "lambda_l2": 0.0,
                              "verbose": -1,
                              "num_threads": 1,
                              **params},
                            train_set,
                            valid_sets=valid_sets,
                            valid_names=valid_names,
                            evals_result=evals_result,
                            verbose_eval=False,
                            callbacks=None)

        score = evals_result['train'][params['objective']][-1]

        return gbm, score

    def predict(self, gbm, dataset):
        ypred = gbm.predict(dataset.data)
        df = pd.DataFrame({'forecast': ypred}, index=dataset.data.index)
        return df




Use your model locally
----------------------

Using and testing your model locally is easy, just create an instance of your class and call its methods as you normally would.

::

  model = MyModel()
  df = model.load_data()
  train_set = model.preprocess(df)





Deploy to a site
----------------

Use :meth:`rebase.api.backend.create` to **CREATE** this model for the specified site

::

  site_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3'
  rb.create(site_id, MyModel)

Use :meth:`rebase.api.backend.update` to **UPDATE** the model code for a specific model

::

  class MyNewModel(rb.Model):
      # your code
      ...

  model_id = '4ab82692-3944-4069-9cbb-f9c59513c1c3'
  rb.update(model_id, MyNewModel)


When to use create vs update?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can have multiple models for a site.

- Use  :meth:`rebase.api.backend.create` if you want to add a new model.
- Use  :meth:`rebase.api.backend.update` if you want to replace the existing model.


Start the model training
------------------------

First, make sure that you have uploaded observation data to train on for the site: :ref:`upload_data`

Use :meth:`rebase.api.backend.train` to start training a specified model. The training period is defined by **start_date** and **end_date**

This will run your class' train() method within the REBASE cloud.

::

  from datetime import datetime

  model_id = 'd9ed55d2-4c7f-4486-a55d-fba8cb2c8791'
  start_date = datetime(2020, 2, 3, 0, 0)
  end_date = datetime(2021, 1, 4, 0, 0)

  rb.train(model_id, start_date, end_date)


When the model is trained successfully, a forecast with the latest data will automatically be generated. See how to get your forecasts here: :ref:`get_site_forecast`
