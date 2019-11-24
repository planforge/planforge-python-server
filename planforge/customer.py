from requests.exceptions import ConnectionError

from planforge.api_requestor import ApiRequestor


class Customer:
    @classmethod
    def all(cls):
        # TODO: paginate
        api = ApiRequestor()
        data = api.get("/customers")

        all = []
        for d in data:
            from planforge import store

            store.put(d["id"], d)
            all.append(cls(d))

        return all

    # TODO: iter

    @classmethod
    def get(cls, id, force=False):
        from planforge import store

        data = store.get(id)

        api = ApiRequestor()
        if not data or force:
            try:
                data = api.get(f"/customers/{id}")
            except ConnectionError:
                pass
            else:
                store.put(id, data)

        if not data:
            data = {}

        return cls(data)

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
