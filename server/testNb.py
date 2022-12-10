from mongoConnection import MongoConnection
import pandas as pd
import os
import json

def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

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


if __name__ == "__main__":
    db = MongoConnection()
    ma_list = [10,50]
    max_drawdown = 0
    win_loss = 0
    exp_profit = 0 


    #df = pd.DataFrame(res)
    currentPath = os.path.abspath(os.getcwd())
    with open(os.path.abspath(os.path.join(currentPath, "server", "cache", "cachedata.json")),"r") as f:
                data = json.load(f)

    f.close()

    print(data)

    df = pd.DataFrame(data["data"])
    df.rename(columns = {'x':'Time'}, inplace = True)
    split = pd.DataFrame(df["y"].tolist(),columns=["Open","High","Low","Close"])
    df = pd.concat([df,split], axis=1)
    df = df.drop("y", axis=1)

    print(df)

    df_ma = df.copy()
    for ma in ma_list:
        df_ma[f'MA_{ma}'] = df_ma.Close.rolling(window=ma).mean() #Create the moving average column
        
    df_ma['DIFF'] = df_ma.MA_10 - df_ma.MA_50 # create a new column that takes the different between the two moving averages
    df_ma['DIFF_PREV'] = df_ma.DIFF.shift(1) # creates a new column that shifts down the diff column, used to determine if there will be a trade
    df_ma['IS_TRADE'] = df_ma.apply(is_trade, axis=1) #Lets you know if you should've made trade based on strategy.

    df_trades = df_ma[df_ma.IS_TRADE!=0].copy() # Creates a dataframe to analyzes all entries that you should've traded... for later stats 

    print(df_ma.tail())