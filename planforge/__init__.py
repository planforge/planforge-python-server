import json

from .api_requestor import ApiRequestor
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


def load_from_file(path):
    with open(path, "r") as json_file:
        return load_from_json(json_file.read())


def load_from_json(json_str):
    data = json.loads(json_str)
    for entry in data:
        Customer.store(entry)


def get_all_data():
    api_requestor = ApiRequestor(api_base, server_key)
    url = api_base + "/customers"
    while url:
        data = api_requestor.request(url).json()
        for entry in data["results"]:
            Customer.store(entry)
        url = data["next"]
    return store.all()
