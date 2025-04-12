from pymongo import MongoClient

def get_db(env):
    CONNECTION_STRING = env["MONGO_CONNECTION_STRING"]
    client = MongoClient(CONNECTION_STRING)
    return client['filedrop_db']

if __name__ == '__main__':
    filedrop_db = get_db()

