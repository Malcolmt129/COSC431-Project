from mongoConnection import MongoConnection
from logging import raiseExceptions
import requests
import datetime
import calendar
import json



def addFromCAPI(timeStart, timeEnd, apiKey, addToDB):
    
    db = MongoConnection() # Creating a connection to ETH financial collection
    COINAPIURL = "https://rest.coinapi.io/v1/exchangerate/ETH/USD/history"
    response = requests.get(COINAPIURL,
    params={'period_id': '4HRS',
            'time_start': timeStart,
            'time_end': timeEnd,
            'limit':2000,
            'apikey': apiKey}
            )
    jsonResponse = response.json()

    if response:
        print("Request Successful. Parsing Response...")
        jsonResponse = generateJsonFile(jsonResponse)
        data = json.loads(jsonResponse[1])
        if addToDB:
            db.addManyDB(data["data"])
        
        return jsonResponse[1]

    else:
        errorString = "Error Requesting Coin API. Error Code: "+str(response.status_code)+". Reason: "+jsonResponse["error"]
        raise Exception(errorString)
    
def generateJsonFile(response):
    hourlyEntryList = {"data" : []}

    for hourlyEntry in response:
        formattedData = formatDataResponse(hourlyEntry)
        hourlyEntryList["data"].append(formattedData)
        
    jsonData = json.dumps(hourlyEntryList, indent=2)
    
    return True, jsonData


def formatDataResponse(data):
    timeString = data["time_period_end"]
    epochTime = calendar.timegm(datetime.datetime.strptime(timeString[:-2], "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    responseData = {
        "x": epochTime,
        "y": [data["rate_open"], data["rate_high"],
        data["rate_low"], data["rate_close"]]
    }
    

    return responseData
addFromCAPI("2021-12-01","2022-11-30","1E869C6C-3CEB-4F6E-B6A9-37214A271D1C", False)
    


if __name__ == "__main__" :
    db = MongoConnection()
    
        # Basically so we can open connections automatically
    def __enter__(self):
        return self
    
    # And automatically close when we are done.
    # Mongo doesn't allow too many connection to
    # the database
    def __exit__(self):
        self.client.close()
        print("DB Client Closed!")