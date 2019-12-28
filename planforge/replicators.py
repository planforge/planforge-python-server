import json
import time
from threading import Thread

import planforge
from planforge.api_requestor import ApiRequestor
from planforge.util import log_debug, log_info


class PollingReplicator(Thread):
    def __init__(self, store, interval=1000, page_limit=100, api_base=None, server_key=None, stripe_livemode=None):
        super().__init__()
        self.daemon = True
        self.store = store
        self.interval = interval
        self.page_limit = page_limit

        api_base = api_base or planforge.api_base
        server_key = server_key or planforge.server_key
        stripe_livemode = stripe_livemode or planforge.stripe_livemode
        self.api_requestor = ApiRequestor(api_base, server_key, stripe_livemode)

    def run(self):
        log_info("Starting polling replicator")
        self._running = True
        self.poll()

    def stop(self):
        log_info("Stopping polling replicator")
        self._running = False

    def poll(self):
        # TODO: catch all exceptions/error codes and continue
        if not self._running:
            log_info("Polling replicator stopped")
            return

        next_page = True
        while next_page:
            current_revision = self.store.revision()
            response = self.api_requestor.get("/state/events", {
                "after_revision": current_revision,
                "limit": self.page_limit,
            })

            for event in response["results"]:
                self.handle_event(event)

            next_page = response["next"]

        time.sleep(self.interval / 1000)
        self.poll()

    def handle_event(self, event):
        if event["action"] == "set":
            self.store.set(event["key"], event["value"])
        elif event["action"] == "delete":
            self.store.delete(event["key"])
        self.store.set("_rev", event["revision"])
