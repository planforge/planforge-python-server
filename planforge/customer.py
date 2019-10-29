from requests.exceptions import ConnectionError

from planforge.api_requestor import ApiRequestor

class Customer:

    @classmethod
    def all(cls):
        api = ApiRequestor()
        data = api.get('/customers')

        all = []
        for d in data:
            from planforge import store
            store.put(d['id'], d)
            all.append(cls(d))

        return all

    @classmethod
    def get(cls, id, force=False):
        from planforge import store
        data = store.get(id)

        api = ApiRequestor()
        if not data or force:
            try:
                data = api.get(f'/customers/{id}')
            except ConnectionError:
                pass
            else:
                store.put(id, data)

        if not data:
            data = {}

        return cls(data)

    def __init__(self, data):
        self.data = data

    def _get_feature(self, key):
        features = self.data.get('features')
        if not features:
            return None

        return next((f for f in features if f['slug'] == key), None)

    def feature_enabled(self, key):
        feature = self._get_feature(key)
        if feature and feature['enabled']:
            return True
        return False
