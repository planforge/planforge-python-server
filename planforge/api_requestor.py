import requests

import planforge
from planforge.errors import PlanForgeApiException
from planforge.util import log_debug


class ApiRequestor:
    def __init__(self, api_base=None, server_key=None):
        self.api_base = api_base or planforge.api_base
        self.server_key = server_key or planforge.server_key

    def get(self, path, params={}):
        return self.request(self.api_base + path, params).json()

    def request(self, url, params={}):
        log_debug("GET %s", url)
        response = requests.get(
            url, params=params, headers={"Authorization": "Bearer " + self.server_key},
        )

        if response.status_code > 299:
            raise PlanForgeApiException(response.json())
        else:
            return response
