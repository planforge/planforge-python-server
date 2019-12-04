from collections import defaultdict

from planforge.rwlock import RWLock
from planforge.util import log_debug


class MemoryStore:
    def __init__(self):
        self._data = defaultdict(dict)
        self._lock = RWLock()

    def all(self):
        log_debug("MemoryStore.all")
        with self._lock.r_locked():
            return list(self._data.values())

    def get(self, key):
        log_debug("MemoryStore.get %s", key)
        with self._lock.r_locked():
            return self._data.get(key)

    def put(self, key, data):
        log_debug("MemoryStore.put %s", key)
        with self._lock.w_locked():
            self._data[key] = data
            return data

    def delete(self, key):
        log_debug("MemoryStore.delete %s", key)
        with self._lock.w_locked():
            del self._data[key]
            return True

    def clear(self):
        log_debug("MemoryStore.clear")
        with self._lock.w_locked():
            self._data = defaultdict(dict)
            return True
