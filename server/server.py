from flask import Flask
from logging import raiseExceptions
import requests
import datetime
import calendar
import json
import sys
import os
from mongoConnection import MongoConnection
from flask_cors import CORS

#graphdata Requires 3 Arguments: Start Time, End Time, and API Key.
#Time Uses The Following Format (Passed as String): YYYY-MM-DDThh:mm:ss OR YYYY-MM-DD
#Please have the User Pass Their Own API Key. An Exception Will Raise If Incorrect

#NOTE: Currently this script returns a JSON file based off Data by the Hour.
#In the future, this script will accomadate for different time rates. When this happens,
#an extra argument will be passes for the time rate

#SAMPLE TIME START: "2016-01-01T00:00:00"
#SAMPLE TIME END: "2016-01-02T00:00:00"

app = Flask(__name__)
CORS(app)


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


@app.route("/graphdata/<timeStart>/<timeEnd>/<apiKey>/<addToDB>")
def test(timeStart, timeEnd, apiKey, addToDB):
    
    db = MongoConnection() # Creating a connection to ETH financial collection
    COINAPIURL = "https://rest.coinapi.io/v1/exchangerate/ETH/USD/history"
    response = requests.get(COINAPIURL,
    params={'period_id': '1HRS',
            'time_start': timeStart,
            'time_end': timeEnd,
            'apikey': apiKey}
            )
    jsonResponse = response.json()

    if response:
        print("Request Successful. Parsing Response...")
        jsonResponse = generateJsonFile(jsonResponse)
        data = json.loads(jsonResponse[1])
        #if addToDB:
        #    db.addManyDB(data)
        currentPath = os.path.abspath(os.getcwd())
        
        with open(os.path.abspath(os.path.join(currentPath, "server", "cache", "cachedata.json")),"w") as f:
            json.dump(data, f)
        f.close()

        return jsonResponse[1]

    else:
        errorString = "Error Requesting Coin API. Error Code: "+str(response.status_code)+". Reason: "+jsonResponse["error"]
        raise Exception(errorString)


if __name__ == "__main__":
    app.run(debug=True)
    

    
