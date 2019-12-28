from collections import defaultdict

from planforge.rwlock import RWLock
from planforge.replicators import PollingReplicator
from planforge.util import log_debug


class BaseStore:

    _replicator = None

    def start(self, replicator_cls=PollingReplicator, replicator_kwargs={}):
        self._replicator = replicator_cls(self, **replicator_kwargs)
        self._replicator.start()

    def stop(self):
        self.teardown()

    def revision(self):
        return int(self.get("_rev", 0))

    def __del__(self):
        self.teardown()

    def teardown(self):
        if self._replicator:
            self._replicator.stop()
            self._replicator = None


class MemoryStore(BaseStore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = defaultdict(dict)
        self._lock = RWLock()

    def all(self):
        log_debug("MemoryStore.all")
        with self._lock.r_locked():
            return list(self._data.values())

    def get(self, key, default=None):
        log_debug("MemoryStore.get %s", key)
        with self._lock.r_locked():
            return self._data.get(key, default)

    def set(self, key, data):
        log_debug("MemoryStore.set %s", key)
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
