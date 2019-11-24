from collections import defaultdict

from .rwlock import RWLock


class MemoryStore:
    def __init__(self):
        self._data = defaultdict(dict)
        self._lock = RWLock()

    def get(self, key):
        with self._lock.r_locked():
            return self._data.get(key)

    def put(self, key, data):
        with self._lock.w_locked():
            self._data[key] = data
            return data

    def delete(self, key):
        with self._lock.w_locked():
            del self._data[key]
            return True

    def clear(self):
        with self._lock.w_locked():
            self._data = defaultdict(dict)
            return True
