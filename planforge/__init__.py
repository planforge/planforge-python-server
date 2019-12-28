import json

from .api_requestor import ApiRequestor
from .customer import Customer
from .stores import MemoryStore
from .streaming import StreamingClient

api_base = "https://www.planforge.io/api"
server_key = None
store = MemoryStore()
stripe_livemode = None
log = None


def load_from_file(path):
    with open(path, "r") as json_file:
        return load_from_json(json_file.read())


def load_from_json(json_str):
    data = json.loads(json_str)
    for entry in data:
        Customer.store(entry)
