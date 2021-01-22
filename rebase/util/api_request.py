import requests
import rebase as rb

def get(path, **kwargs):
    headers = {'Authorization': rb.api_key, 'GL-API-KEY': rb.api_key}
    url = rb.base_api_url+path
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
    url = rb.base_api_url+path
    response = requests.post(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response

def delete(path, **kwargs):
    headers = {'Authorization': rb.api_key, 'GL-API-KEY': rb.api_key,}
    url = rb.base_api_url+path
    response = requests.delete(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response
