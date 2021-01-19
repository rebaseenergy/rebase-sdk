import rebase.util.api_request as api_request
import requests
import json
import dill



def create(site_id, model):
    data = dill.dumps(model, recurse=True)

    params = {'model_name': model.__name__}
    path = 'platform/v1/model/custom/create/{}'.format(site_id)
    r = api_request.post(path, params=params, data=data)
    return r.json()


def update(model_id, model):
    path = 'platform/v1/model/custom/update/{}'.format(model_id)
    r = api_request.post(path, data=model)
    return r.json()


def train(model_id, start_date, end_date):
    path = 'platform/v1/model/train/{}'.format(model_id)
    data = {
        'start_date': start_date,
        'end_date': end_date
    }
    r = api_request.post(path, data=json.dumps(data))
    print(r.status_code)
