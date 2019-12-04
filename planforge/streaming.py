import asyncio
import json
import websockets
from threading import Thread

import planforge
from planforge.util import log_debug, log_info


class StreamingClient(Thread):
    def __init__(self, streaming_endpoint=None, server_key=None):
        super().__init__()
        self.daemon = True
        self.streaming_endpoint = streaming_endpoint or planforge.streaming_endpoint
        self.server_key = server_key or planforge.server_key

    def run(self):
        log_info("Starting event stream")
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.stream())

    def stop(self):
        log_info("Stopping event stream")
        if self.loop:
            self.loop.stop()
            self.loop.close()
        self.loop = None
        log_info("Event stream stopped")

    async def stream(self, retry_delay=1):
        while True:
            try:
                await self._stream()
            except (
                OSError,
                asyncio.TimeoutError,
                websockets.exceptions.ConnectionClosedError,
            ):
                await asyncio.sleep(retry_delay)
                log_debug("Websocket connection closed, retrying...")
                continue

    async def _stream(self):
        log_debug("Opening websocket connection to %s", self.streaming_endpoint)
        async with websockets.connect(
            self.streaming_endpoint,
            extra_headers={"Authorization": "Bearer " + self.server_key},
        ) as websocket:
            async for event in websocket:
                self.handle_event(json.loads(event))

    def handle_event(self, event):
        from planforge import store

        if event["action"] == "put":
            store.clear()
            for entry in event["data"]:
                store.put(entry["id"], entry)
        elif event["action"] == "patch":
            store.put(event["data"]["id"], event["data"])
        elif event["action"] == "delete":
            store.delete(event["data"]["id"])
