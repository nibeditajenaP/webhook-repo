from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def insert_event(data):
    collection.insert_one(data)

def get_latest_events(limit=10):
    return list(collection.find().sort("timestamp", -1).limit(limit))
