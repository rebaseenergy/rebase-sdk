from rebase.error import InvalidInputError, NotFoundError
import rebase.util.api_request as api_request
import json

class Layer():

    base_path = 'platform/v1'

    @classmethod
    def create(cls, packages):
        path = '{}/layer/create'.format(cls.base_path)
        data = json.dumps({'packages': packages})
        response = api_request.post(path, data=data)
        if response.status_code == 400:
            raise InvalidInputError(response.text)
        return response.json()

    @classmethod
    def delete(cls, id):
        path = '{}/layer/{}'.format(cls.base_path, id)
        response = api_request.delete(path)
        if response.status_code == 404:
            raise NotFoundError(response.text)
        print(response.text)

    @classmethod
    def get(cls, id):
        path = '{}/layer/{}'.format(cls.base_path, id)
        response = api_request.get(path)
        if response.status_code == 404:
            raise NotFoundError(response.text)
        return response.json()

    @classmethod
    def list(cls):
        path = '{}/layer/list'.format(cls.base_path)
        response = api_request.get(path)
        return response.json()

    @classmethod
    def status(cls, id):
        path = '{}/layer/status/{}'.format(cls.base_path, id)
        response = api_request.get(path)
        if response.status_code == 404:
            raise NotFoundError(response.text)
        return response.json()
