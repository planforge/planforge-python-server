import json
import os

from requests.exceptions import ConnectionError

from planforge.api_requestor import ApiRequestor


class PlanForgeObject(dict):
    def __setattr__(self, k, v):
        self[k] = v

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

    def __delattr__(self, k):
        del self[k]


class Customer(PlanForgeObject):
    @classmethod
    def retrieve(cls, id, api_base=None, server_key=None, force=False):
        from planforge import store

        data = store.get(id)
        if not data or force:
            cls.request(id, api_base=api_base, server_key=server_key)
        return cls(store.get(id))

    @classmethod
    def request(cls, id, api_base=None, server_key=None):
        from planforge import store

        api = ApiRequestor(api_base=api_base, server_key=server_key)
        # TODO: handle exception
        data = api.get(f"/customers/{id}")
        cls.store(data)

    @classmethod
    def store(id, data):
        from planforge import store

        store.put(data["id"], data)

    def feature(self, key):
        features = self.get("features", [])
        for feature in features:
            if feature["slug"] == key:
                return CustomerFeature(feature)
        return CustomerFeature()


class CustomerFeature(PlanForgeObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.get("enabled") is None:
            self["enabled"] = False
