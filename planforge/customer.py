import json
import os

from requests.exceptions import ConnectionError

from planforge.api_requestor import ApiRequestor


class Customer:
    @classmethod
    def get(cls, id, api_base=None, server_key=None, force=False):
        from planforge import store

        data = store.get(id)
        if not data or force:
            try:
                api = ApiRequestor(api_base=api_base, server_key=server_key)
                data = api.get(f"/customers/{id}")
            except ConnectionError as e:
                print(e)
            else:
                store.put(id, data)

        if not data:
            data = {}

        return cls(data)

    @classmethod
    def from_file(cls, path):
        abs_path = os.path.join(os.getcwd(), path)
        with open(abs_path, "r") as json_file:
            json_string = json_file.read()
            return cls.from_json(json_string)

    @classmethod
    def from_json(cls, json_string):
        from planforge import store

        data = json.loads(json_string)
        ret = []
        for d in data:
            store.put(d["id"], d)
            ret.append(cls(d))
        return ret

    def __init__(self, data):
        self.data = data

    def _get_feature_data(self, key):
        features = self.data.get("features")
        if not features:
            return None

        return next((f for f in features if f["slug"] == key), None)

    def feature(self, key):
        data = self._get_feature_data(key)
        return CustomerFeature(data)


class CustomerFeature:

    enabled = False
    slug = ""
    subscription_id = ""

    def __init__(self, data):
        if data:
            self.enabled = data["enabled"]
            self.slug = data["slug"]
            self.subscription_id = data.get("subscription", None)
