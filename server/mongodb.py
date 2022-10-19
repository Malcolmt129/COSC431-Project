from typing import Collection
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://Username:Password@cosc431.mku33pu.mongodb.net/?retryWrites=true&w=majority")
db = cluster["ETH"]
collection = db["ETH"]

