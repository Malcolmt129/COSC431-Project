from pymongo import MongoClient
import json 

class MongoConnection:
    
   # Initializes the connection to the collection. Collection is a 
   # parameter, because we currently have 2, one for the ETH data
   # and one for the users. So this is allows you to pick one.
   
    def __init__(self) -> None:
        self.connection_str ="mongodb+srv://Username:Password@class.vrz5xva.mongodb.net/test"
        self.client = MongoClient(self.connection_str)
        self.db = self.client["ETH"]
        self.collection = self.db["ETH"]
        
        
    # Basically so we can open connections automatically
    def __enter__(self):
        return self
    
    # And automatically close when we are done.
    # Mongo doesn't allow too many connection to
    # the database
    def __exit__(self):
        self.client.close()
        print("DB Client Closed!")
        

    def addOneDB (self, data):
        self.collection.insert_one(data) #Add one entry to DB
        
    def addManyDB(self,data):
        self.collection.insert_many(data) #Add multiple entries to DB

    def deleteAll(self):
        self.collection.delete_many({}) # Used for testing purposes to quickly remove all entries.
        
    def query_from_to(self, start, end):
        result = self.collection.find({"x" : {"$gte" : start , "$lte" : end}}, {"_id":0, "x":1, "y":1})
        data = []
        for candle in result:
            data.append(candle)
            
        return data
        
        
        

if __name__ == "__main__":
    
    db = MongoConnection()
    #db.deleteAll()
    # Only use this code if you want to delete all inputs
    