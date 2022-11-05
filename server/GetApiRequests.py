from logging import raiseExceptions
import requests
import datetime
import calendar
import json
import sys
import os
from mongoConnection import MongoConnection

#This Script Requires 3 Arguments: Start Time, End Time, and API Key.
#Time Uses The Following Format (Passed as String): YYYY-MM-DDThh:mm:ss OR YYYY-MM-DD
#Please have the User Pass Their Own API Key. An Exception Will Raise If Incorrect

#EXAMPLE CALL: python getRequestData.py "Start Time" "End Time" "API Key"

#NOTE: Currently this script creates a JSON file based off Data by the Hour.
#In the future, this script will accomadate for different time rates. When this happens,
#an extra argument will be passes for the time rate

#SAMPLE TIME START: "2016-01-01T00:00:00"
#SAMPLE TIME END: "2016-01-02T00:00:00"




def generateJsonFile(response):
    hourlyEntryList = []

    for hourlyEntry in response:
        formattedData = formatDataResponse(hourlyEntry)
        hourlyEntryList.append(formattedData)
        
    jsonData = json.dumps(hourlyEntryList, indent=2)

    currentDirectory = os.getcwd()
    jsonSaveLocation = os.path.join(currentDirectory, "JsonData")
    with open(os.path.join(jsonSaveLocation, "jsonData.json"), "w") as f:
        f.write(jsonData)
        f.close()
    
    return True, jsonData


def formatDataResponse(data):
    timeString = data["time_period_end"]
    epochTime = calendar.timegm(datetime.datetime.strptime(timeString[:-2], "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    responseData = {
        "x": epochTime,
        "y": {"open":data["rate_open"], "high":data["rate_high"],
        "low":data["rate_low"], "close":data["rate_close"]}
    }
    

    return responseData


if __name__ == "__main__":
    
    if len(sys.argv) != 4:
        raise Exception("Error calling Script. GetApiRequests.py takes 3 arguments. "+str(len(sys.argv)-1)+" passed.")

    db = MongoConnection("ETH") # Creating a connection to ETH financial collection
    COINAPIURL = "https://rest.coinapi.io/v1/exchangerate/ETH/USD/history"
    timeStart = sys.argv[1]
    timeEnd = sys.argv[2]
    apiKey = sys.argv[3]

    response = requests.get(COINAPIURL,
    params={'period_id': '1HRS',
            'time_start': timeStart,
            'time_end': timeEnd,
            'apikey': apiKey}
            )
    jsonResponse = response.json()

    if response:
        print("Request Successful. Parsing Response...")
        jsonFile = generateJsonFile(jsonResponse)
        
        data = json.loads(jsonFile[1])
        db.addManyDB(data)
        
        if jsonFile:
            print("Response Parsed. Sucessfully Generated Json File.")

    else:
        errorString = "Error Requesting Coin API. Error Code: "+str(response.status_code)+". Reason: "+jsonResponse["error"]
        raise Exception(errorString)
    
    sentinel = input("Check mongo Atlas to see if changes were made, do you want to delete all entries now? y/n ")
    
    if (sentinel.lower == "y"):
        db.deleteAll()
    else:
        pass
    