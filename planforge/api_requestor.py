import requests
from planforge.errors import PlanForgeApiException

class ApiRequestor:
    def __init__(self):
        from planforge import api_url, api_key
        self.api_url = api_url
        self.api_key = api_key

    def get(self, url, params={}):
        response = requests.get(self.api_url + url, params=params, headers={
            'Authorization': 'Bearer ' + self.api_key,
        })

        if response.status_code > 299:
            raise PlanForgeApiException(response.json())
        else:
            return response.json()
