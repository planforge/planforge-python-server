from .customer import Customer
from .stores import MemoryStore

api_base = "https://www.planforge.io/api"
server_key = None
store = MemoryStore()
streaming_base = "wss://www.planforge.io./rt"
