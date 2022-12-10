from flask import Flask
from logging import raiseExceptions
import datetime
import calendar
import json
import pandas as pd
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


def getEpochTime(desiredTime):
    if "T" in desiredTime:
        epochTime = calendar.timegm(datetime.datetime.strptime(desiredTime, "%Y-%m-%dT%H:%M:%S.%f").timetuple())
    else:
        epochTime = calendar.timegm(datetime.datetime.strptime(desiredTime, "%Y-%m-%d").timetuple())
    
    return epochTime

@app.route("/graphdata/<timeStart>/<timeEnd>/<apiKey>/<addToDB>")
def test(timeStart, timeEnd, apiKey, addToDB):
    db = MongoConnection()  

    startEpoch = getEpochTime(timeStart)
    endEpoch = getEpochTime(timeEnd)
    response = db.query_from_to(startEpoch, endEpoch) #Returns iterable cursor Object

    print("Request Successful. Parsing Response...")

    data = {"data":response}
    currentPath = os.path.abspath(os.getcwd())
    
    with open(os.path.abspath(os.path.join(currentPath, "server", "cache", "cachedata.json")),"w") as f:
        json.dump(data, f)
    f.close()

    return data



@app.route("/tradedata")
def run():
    
    ma_list = [10,50]
    return_dict = {}
    
    #Creates the dataframe
    df = query2DF()
    print(df)
    df_ma = makeMA_plot(df,ma_list)
    print(df_ma)
    trades = findTrades(df_ma)
    print(trades)
    #Gets the stats
    exp_profit = getProfit(trades)
    print(exp_profit)
    max_drawdown = max_draw(trades["GAIN"])
    print(max_drawdown)
    win_loss = winCount(trades["GAIN"]) / (len(trades)-1)
    max_win = getLargestWin(trades["GAIN"])
    max_loss = getLargestLoss(trades["GAIN"])
    
    #build the return dict for the frontend 
    return_dict["profits"] = exp_profit
    return_dict["max_drawdown"] = max_drawdown
    return_dict["win_loss"] = win_loss
    return_dict["max_loss"] = max_loss
    return_dict["max_win"] = max_win

    
    return return_dict


def query2DF():
    #db = MongoConnection()
    #res = db.query_from_to(1638331200,1641196800) #Returns iterable cursor Object

    currentPath = os.path.abspath(os.getcwd())
    with open(os.path.abspath(os.path.join(currentPath, "server", "cache", "cachedata.json")),"r") as f:
                res = json.load(f)

    f.close()

    df = pd.DataFrame(res["data"]) #makes dataframe
    df.rename(columns = {'x':'Time'}, inplace = True) #Renames x column to Time in df
    split = pd.DataFrame(df["y"].tolist(),columns=["Open","High","Low","Close"]) # Splits the y array into appropriate candle parts in df
    df = pd.concat([df,split], axis=1) #Brings the previous 
    df = df.drop("y", axis=1)
    
    return df


def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

def makeMA_plot(df,ma_list):
        df_ma = df.copy()
        for ma in ma_list:
            df_ma[f'MA_{ma}'] = df_ma.Close.rolling(window=ma).mean() #Create the moving average column
        
        df_ma['DIFF'] = df_ma.MA_10 - df_ma.MA_50 # create a new column that takes the different between the two moving averages
        df_ma['DIFF_PREV'] = df_ma.DIFF.shift(1) # creates a new column that shifts down the diff column, used to determine if there will be a trade
        df_ma['IS_TRADE'] = df_ma.apply(is_trade, axis=1) #Lets you know if you should've made trade based on strategy.
        
        return df_ma

def findTrades(df_ma):
    df_trades = df_ma[df_ma.IS_TRADE!=0].copy() # Creates a dataframe to analyzes all entries that you should've traded... for later stats 
    df_trades["DELTA"] = df_trades.Close.diff().shift(-1)
    df_trades["GAIN"] = df_trades["DELTA"] * df_trades["IS_TRADE"]
    
    return df_trades
    

def max_draw(row):
    local_max = 0
    max_drawdown = 0
    for num in row:
        if num < 0:
            local_max+=num
            if local_max < max_drawdown:
                max_drawdown = local_max
        else:
            local_max = 0
    return max_drawdown

def winCount(row):
    count = 0
    for num in row:
        if num >= 0:
            count+=1
    return count

def getProfit(df):
    return df["GAIN"].sum()

def getLargestWin(row):
    return row.max()

def getLargestLoss(row):
    return row.min()
    



if __name__ == "__main__":
    app.run(debug=True)
    

    
