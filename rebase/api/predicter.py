import rebase as rb
import pickle
from datetime import datetime
import rebase.util.api_request as api_request


class Predicter():

    @classmethod
    def load_data(cls, pred, start_date, end_date):
        site_config = rb.Site.get(pred.site_id)
        return pred.load_data(site_config, start_date, end_date)


    @classmethod
    def load_latest_data(cls, predicter):
        Predicter.load_data(predicter)


    @classmethod
    def train(cls, pred, params, start_date, end_date):
        weather_df, observation_df = Predicter.load_data(pred, start_date, end_date)
        dataset = pred.preprocess(weather_df, observation_df)
        return pred.train(dataset, params)

    @classmethod
    def hyperparam_search(self, pred, params_list):
        models = []
        for p in params_list:
            model, score = pred.train(dataset, p)


    @classmethod
    def deploy(cls, pred):
        print("Deploying {}".format(pred.name))
        path = 'platform/v1/site/train/{}'.format(pred.site_id)

        response = api_request.post(path)
        if response.status_code == 200:
            print("Success!")
        else:
            print("Failed")

    @classmethod
    def predict(cls, pred):
        Predicter.load_latest_data()


    @classmethod
    def status(cls, pred):
        path = '/platform/v1/site/train/state/{}'.format(pred.site_id)
        r = api_request.get(path)

        status = {'status': None, 'history': []}
        if r.status_code == 200:
            data = r.json()
            if len(data) > 0:
                status['status'] = data[-1]['state']
                status['history'] = data
        return status




class Model():

    def setup(self):
        pass


    def load_data(self, site_config, start_date, end_date):
        """This method should load the data for training

        Args:
            site_config (dict): config for the site
            start_date (datetime): the start date for the period
            end_date (datetime): the end date for the period

        Returns:
            - pd.DataFrame: one df
            - pd.DataFrame: one df

        """

        raise NotImplementedError(
            'Your subclass must implement the load_data() method'
        )

    def load_latest_data(self, site_config):
        """This method should load the predict data for training

        Args:
            site_config (dict): config for the site

        Returns:

        """

        raise NotImplementedError(
            'Your subclass must implement the load_data() method'
        )

    def preprocess(self, weather_data, observation_data=None):
        raise NotImplementedError(
            'Your subclass must implement the preprocess() method'
        )

    def train(self, train_set, params={}):
        raise NotImplementedError(
            'Your subclass must implement the train() method'
        )


    # weather_df - weather for a ref time
    # target_observations - like recent production power, could be used for intraday
    def predict(self, predict_set):
        raise NotImplementedError(
            'Your subclass must implement the predict() method'
        )

    # serialize() should be overriden with custom serialization
    # method if @param model can't be pickled
    def serialize(self, model):
        return pickle.dumps(model)

    # deserialize() should be overriden with custom deserialization method
    # if @param serialized_model can't be loaded from pickle
    def deserialize(self, serialized_model):
        return pickle.loads(serialized_model)
