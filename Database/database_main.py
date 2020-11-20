import requests
import csv
import json
import pandas as pd
import datetime as dt
import sys
import os
import pymongo


class Database(object):
    
 
    def read_tickers(tickerType):
        ##get the tickers for all stocks in the index
        #sp = pd.read_csv(tickerfile) #(r'S&P500Tickers.csv')
        #tickers = sp.Symbol
        #return tickers
        client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
        db = client.MIE479
        if (tickerType == 1):
            collection = db.SP500Tickers
        elif (tickerType == 2):
            collection = db.SP1500Tickers
        elif(tickerType == 3):
            collection = db.ETFTickers
            
        data = collection.find()
        tickers = [];
        for item in data:
            tickers.append(item["Symbol"])
        return tickers
        
    def get_date():
        #set the time interval for getting the stock price
        dtToDate = '2020-09-30' #str(dt.datetime.now().date())
        dtFromDate = '2010-09-30'
        dates = [dtFromDate, dtToDate]
        return dates
    
    
    def get_price(tickers,dates):
        #get the weekly historical price for each stock
        headers = {'Content-Type': 'application/json'}
    
        table =[];
        for i in range(0,len(tickers)):
            requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/"+tickers[i]+"/prices?startDate="+dates[0]+"&endDate="+dates[1]+"&token=6b6dca5492e46a79e40f578eb6ecafe357ddc31b&resampleFreq=weekly")
            temp_list = requestResponse.json()
            print(tickers[i])
            dict = {};
            list = requestResponse.json()
            dict['Symbol'] = tickers[i]
            for j in range(0,len(list)):
                #print(list[j])
                longdate = list[j]['date']
                date = longdate[0:10]
                #print(date)
                dict[date] = list[j]['adjClose']  
            table.append(dict);
        return table
    
    def write_csv(table,pricefile):
        #Write into csv
        df = pd.DataFrame(table)
        df.to_csv(pricefile, index=False)
    
    
    def import_content(pricefile,collection):
        #import the csv file to MongoDB Atlas
        mng_client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
        mng_db = mng_client['MIE479'] # Replace mongo db name
        collection_name = collection # Replace mongo db collection name
        db_cm = mng_db[collection_name]
        cdir = os.path.dirname(__file__)
        file_res = os.path.join(cdir, pricefile)
    
        data = pd.read_csv(file_res)
        data_json = json.loads(data.to_json(orient='records'))
        db_cm.delete_many({})
        db_cm.insert_many(data_json)
        
    def read_data(collection):
        #read data from Atlas collections
        client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
        db = client.MIE479
        if (collection == 'factors'):
            cursor = db.factors.find()
        elif (collection == 'SP500Tickers'):
            cursor = db.SP500Tickers.find()
        elif (collection == 'SP500Price'):
            cursor = db.SP500AdjClose.find()
        elif (collection == 'SP1500Tickers'):
            cursor = db.SP1500Tickers.find()
        elif (collection == 'SP1500Price'):
            cursor = db.SP1500AdjClose.find()  
        elif (collection == 'ETFTickers'):
            cursor = db.ETFTickers.find()
        elif (collection == 'ETFPrice'):
            cursor = db.ETFAdjClose.find()        
        
        df = pd.DataFrame(list(cursor))
        df = df.drop(['_id'],axis = 1)
        
        return df
        
        
    
    
    ##main function#################################################################
    ##S&P500 stocks
    #pricefile = 'SP500AdjClose.csv' #the file which the adjusted closing price is written into
    #collection = 'SP500AdjClose'  #the file in which the price is stored 
    #tickers = read_file(1) #ticker type 1 = s&p500 tickers
    #dates = get_date()
    #table = get_price(tickers,dates)
    #write_csv(table,pricefile)
    #import_content(pricefile,collection)
    
    ##S&P1500 stocks
    #pricefile = 'SP1500AdjClose.csv' #the file which the adjusted closing price is written into
    #collection = 'SP1500AdjClose'  #the collection in which the price is stored 
    #tickers = read_file(2) #ticker type 2 = S&P1500 tickers
    #dates = get_date()
    #table = get_price(tickers,dates)
    #write_csv(table,pricefile)
    #import_content(pricefile,collection)
    
    ##ETFs
    #pricefile = 'ETFAdjClose.csv' #the file which the adjusted closing price is written into
    #collection = 'ETFAdjClose'  #the collection in which the price is stored 
    #tickers = read_file(3) #ticker type 1 = ETF tickers
    #dates = get_date()
    #table = get_price(tickers,dates)
    #write_csv(table,pricefile)
    #import_content(pricefile,collection)
     
    
    
