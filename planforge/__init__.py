from .customer import Customer
from .stores import MemoryStore
from .streaming import StreamingClient

api_base = "https://www.planforge.io/api"
server_key = None
store = MemoryStore()
streaming_endpoint = "wss://www.planforge.io./rt/client"
streaming_client = None


def start_streaming(streaming_client_class=None):
    global streaming_client
    client_class = streaming_client_class or StreamingClient
    streaming_client = StreamingClient()
    streaming_client.start()


def stop_streaming():
    global streaming_client
    if streaming_client:
        streaming_client.stop()
        streaming_client = None
