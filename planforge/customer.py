from requests.exceptions import ConnectionError

from planforge.api_requestor import ApiRequestor

class Customer:

    @classmethod
    def all(cls):
        api = ApiRequestor()
        data = api.get('/state')

        all = []
        # TODO: refactor to a .items() call
        for id in data:
            from planforge import store
            store.put(id, data[id])
            all.append(cls(data[id]))

        return all

    @classmethod
    def get(cls, id, force=False):
        from planforge import store
        data = store.get(id)

        api = ApiRequestor()
        if not data or force:
            try:
                response = api.get('/state', {'customer': id})
            except ConnectionError:
                pass
            else:
                data = response[id]
                store.put(id, data)

        if not data:
            data = {}

        return cls(data)

    def __init__(self, data):
        self.data = data

    def feature_enabled(self, key):
        if (
            self.data.get('features') and
            self.data['features'].get(key) and
            self.data['features'][key].get('enabled')
        ):
            return True
        return False
