import rebase.util.api_request as api_request
import requests
import json
import dill
import rebase as rb


def create(site_id, model):
    data = dill.dumps(model, recurse=True)

    params = {'model_name': model.__name__}
    path = 'platform/v1/model/custom/create/{}'.format(site_id)
    r = api_request.post(path, params=params, data=data)
    if r.status_code != 200:
        raise Exception(f"Error creating model for site {site_id}: {r.content.decode('utf-8')}")
    return r.json()


def update(model_id, model):
    data = dill.dumps(model, recurse=True)
    params = {'model_name': model.__name__}
    path = 'platform/v1/model/custom/update/{}'.format(model_id)
    r = api_request.post(path, params=params, data=data)
    if r.status_code == 200:
        print('Ok, updated model {}'.format(model_id))
    else:
        raise Exception('Failed updating model {}'.format(model_id))


def train(model_id, start_date, end_date):
    path = 'platform/v1/model/train/{}'.format(model_id)
    data = {
        'start_date': start_date,
        'end_date': end_date
    }
    r = api_request.post(path, data=json.dumps(data))
    if r.status_code != 200:
        raise Exception(f"Error starting train for model {model_id}: {r.content.decode('utf-8')}")
    return r.content.decode('utf-8')


def hyperparam_search(model_id, params={}, hyperparams={}, n_trials=10, compute_params={}):
    path = 'platform/v1/model/hyperparam_search/{}'.format(model_id)
    params['model_id'] = model_id
    params['api_key'] = rb.api_key
    data = {
        'params': params,
        'hyperparams': hyperparams,
        'n_trials': n_trials,
        'compute_params': compute_params
    }
    r = api_request.post(path, data=json.dumps(data))
    if r.status_code != 200:
        raise Exception(f"Error starting hyperparam_search for model {model_id}: {r.content.decode('utf-8')}")
    return r.json()

def report_result(model_id, job_name=None, params={}, score=None, exception=None):
    path = 'platform/v1/model/hyperparam_result/{}'.format(model_id)
    params['model_id'] = model_id
    params['api_key'] = rb.api_key
    data = {
        'job_name': job_name,
        'params': params,
        'score': score,
        'exception': exception
    }
    r = api_request.post(path, data=json.dumps(data))
    if r.status_code != 200:
        raise Exception(f"Error reporting hyperparam result for model {model_id}: {r.content.decode('utf-8')}")
    return r.json()