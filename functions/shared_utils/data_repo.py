from pymongo import MongoClient
import os

class DataRepo():
    def get_db(self):
        CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
        self.DATABASE_NAME = os.environ.get("DATABASE_NAME")

        client = MongoClient(CONNECTION_STRING)
        return client[self.DATABASE_NAME]
    
    def __init__(self, container_id):
        self.db = self.get_db()
        print(f"Initializing repo for container {container_id} from database {self.DATABASE_NAME}")
        self.data = self.db[container_id]

    def search(self, query):
        return self.data.find(query)
    
    def search_one(self, query):
        return self.data.find_one(query)
    
    def create_item(self, item):
        return self.data.insert_one(item)
    
    def delete_item(self, item):
        return self.data.delete_one(item)
    
    def update_item(self, item, key):
        query_filter = {}
        query_filter[key] = item[key]
        return self.data.replace_one(query_filter, item)

    def get_queryable(self):
        return self.data