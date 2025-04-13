from pymongo import MongoClient
import os

class DataRepo():
    def get_db():
        CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
        client = MongoClient(CONNECTION_STRING)
        return client[os.environ.get("DATABASE_NAME")]
    
    def __init__(self, container_id):
        self.db = self.get_db()
        self.data = self.db[container_id]

    def search(self, query):
        return self.data.find(query)
    
    def create_item(self, item):
        return self.data.insert_one(item)
    
    def delete_item(self, item):
        return self.data.delete_one(item)