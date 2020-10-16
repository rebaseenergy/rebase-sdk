import requests
import rebase as rb
from rebase.config import base_api_url

def get(path, **kwargs):
    headers = {'Authorization': rb.api_key, 'GL-API-KEY': rb.api_key}
    url = base_api_url+path
    response = requests.get(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response


def post(path, **kwargs):
    headers = {
        'Authorization': rb.api_key,
        'GL-API-KEY': rb.api_key,
        'Content-Type': 'application/json'
    }
    url = base_api_url+path
    response = requests.post(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response

def delete(path, **kwargs):
    headers = {'Authorization': rb.api_key, 'GL-API-KEY': rb.api_key,}
    url = base_api_url+path
    response = requests.delete(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response
