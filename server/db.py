from pymongo import MongoClient

def get_db():
    CONNECTION_STRING = "mongodb+srv://ajay:ihatedevops@cluster0.fwskhqi.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    return client['filedrop_db']

if __name__ == '__main__':
    filedrop_db = get_db()

