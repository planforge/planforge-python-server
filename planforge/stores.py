from collections import defaultdict

from planforge.api_requestor import ApiRequestor
from planforge.replicators import PollingReplicator
from planforge.rwlock import RWLock
from planforge.util import log_debug


class BaseStore:

    lock_cls = None

    def __init__(self):
        self._lock = self.lock_cls()
        self._replicator = None

    def start(
        self,
        api_base=None,
        server_key=None,
        stripe_livemode=None,
        replicator_cls=PollingReplicator,
        replicator_kwargs={},
    ):
        if self.revision() == 0:
            self.clear()
            self.refresh_state(
                api_base=api_base,
                server_key=server_key,
                stripe_livemode=stripe_livemode,
            )

        self._replicator = replicator_cls(
            self,
            api_base=api_base,
            server_key=server_key,
            stripe_livemode=stripe_livemode,
            **replicator_kwargs
        )
        self._replicator.start()

    def refresh_state(self, api_base=None, server_key=None, stripe_livemode=None):
        state = self.request_state(api_base, server_key, stripe_livemode)
        self.store_state(state)

    def request_state(self, api_base=None, server_key=None, stripe_livemode=None):
        api_requestor = ApiRequestor(api_base, server_key, stripe_livemode)
        return api_requestor.get("/state")

    def stop(self):
        self.teardown()

    def revision(self):
        return self.get("_rev", 0)

    def __del__(self):
        self.teardown()

    def teardown(self):
        if self._replicator:
            self._replicator.stop()
            self._replicator = None


class MemoryStore(BaseStore):
    lock_cls = RWLock

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = defaultdict(dict)

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

    def store_state(self, state):
        log_debug("MemoryStore.store_state")
        with self._lock.w_locked():
            self._data = state
