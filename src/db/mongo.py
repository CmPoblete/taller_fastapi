from pymongo.mongo_client import MongoClient

MONGO_URL = "mongodb://mongodb:27017"

client = MongoClient(MONGO_URL)
db = client["muoh"]
if db["properties"] is None:
    db.create_collection("properties")
