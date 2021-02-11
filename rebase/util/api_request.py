import requests
import rebase as rb
import time
import random

def robust(max_tries=5, retry_statuses=[429]):
    def decorator(func):
        def handle_call(*args, **kwargs):
            n_try = 0
            while True:
                response = func(*args, **kwargs)
                if response.status_code in retry_statuses:
                    if n_try < max_tries:
                        time.sleep(min(2**n_try * (1+random.random()), 300))
                        n_try += 1
                    else:         
                        return response
                else:
                    return response                    
        return handle_call
    return decorator

@robust(max_tries=10, retry_statuses=[429])
def get(path, **kwargs):
    headers = {'Authorization': rb.api_key, 'GL-API-KEY': rb.api_key}
    url = rb.base_api_url+path
    response = requests.get(url, **kwargs, headers=headers)
    if response.status_code == 401:
        raise Exception('Unathorized')

    return response

@robust(max_tries=10, retry_statuses=[429])
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
