import requests

import planforge
from planforge.errors import PlanForgeApiException


class ApiRequestor:
    def __init__(self, api_base=None, server_key=None):
        self.api_base = api_base or planforge.api_base
        self.server_key = server_key

    def get(self, url, params={}, server_key=None):
        if self.server_key:
            _server_key = self.server_key
        else:
            from planforge import server_key

            _server_key = server_key

        response = requests.get(
            self.api_base + url,
            params=params,
            headers={"Authorization": "Bearer " + _server_key,},
        )

        if response.status_code > 299:
            raise PlanForgeApiException(response.json())
        else:
            return response.json()
