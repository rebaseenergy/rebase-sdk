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


#def train(model_id):
#
#    path = 'platform/v1/model/custom/create/{}'.format(site_id)
#    r = api_request.post(path, params=params, data=data)
