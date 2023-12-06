import pymongo
from dotenv import load_dotenv
import os

class MongoDB:

    _client = None
    @classmethod
    def get_client(cls):
        if cls._client is None:
            load_dotenv()
            uri = os.getenv("MONGODB_URI")
            try:
                cls._client = pymongo.MongoClient(uri=uri)
            except Exception as e:
                print(f"Failed to connect to MongoDB {e}")
        return cls._client

    def __init__(self) -> None:
        self.client = self.get_client()
