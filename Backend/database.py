import requests
import csv
import json
import pandas as pd
import datetime as dt
import sys
import os
import pymongo



class DatabaseError(Exception):
    pass

class _Database(object):

    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
        self.db = client.MIE479

    def get_users_count(self, email):
        users = self.db.Users.find({'email': email})
        return users, users.count()

    def get_user(self, email):
        users, counts = self.get_users_count(email)
        if counts == 0:
            return None
        elif counts == 1:
            return users.next()
        
        raise DatabaseError('User does not exist')

    def create_user(self, first_name, last_name, email, salt, master_key):
        if self.get_users_count(email)[1] != 0:
            raise DatabaseError('User already exists')

        user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'salt': salt,
            'master_key': master_key,
        }

        res = self.db.Users.insert_one(user)

        if res.acknowledged:
            return True

        raise DatabaseError('Could not create user')

    def create_session(self, email, session_id, expiration, last_used):
        if self.db.sessions.find({'session_id': session_id}).count() != 0:
            return False

        session = {
            'email': email,
            'session_id': session_id,
            'expiration': expiration,
            'last_used': last_used,
        }

        res = self.db.sessions.insert_one(session)

        if res.acknowledged:
            return True

        raise DatabaseError('Could not create session')

    def clear_sessions(self):
        raise NotImplementedError
        regular = self.db.sessions.find({'expiration': None})
        remembered_sessions = self.db.sessions.find({'expiration': {'$ne': None}})

        

Database = _Database()
DB = Database

#     def read_tickers(self, tickerType):
#         if (tickerType == 1):
#             collection = self.db.SP500Tickers
#         elif (tickerType == 2):
#             collection = self.db.SP1500Tickers
#         elif(tickerType == 3):
#             collection = self.db.ETFTickers
            
#         data = collection.find()
#         tickers = []
#         for item in data:
#             tickers.append(item["Symbol"])
#         return tickers
        
#     def get_date():
#         #set the time interval for getting the stock price
#         dtFromDate = '2005-09-30'
#         dtToDate = '2020-09-30' #str(dt.datetime.now().date())
#         dates = [dtFromDate, dtToDate]
#         return dates
    
    
#     def get_price(tickers,dates):
#         #get the weekly historical price for each stock
#         headers = {
#         'Content-Type': 'application/json'
#         }
    
#         table =[];
#         for i in range(0,len(tickers)):
#             requestResponse = requests.get("https://api.tiingo.com/tiingo/daily/"+tickers[i]+"/prices?startDate="+dates[0]+"&endDate="+dates[1]+"&token=6b6dca5492e46a79e40f578eb6ecafe357ddc31b&resampleFreq=weekly",headers=headers)
#             temp_list = requestResponse.json()
#             dict = {};
#             dict['Symbol'] = tickers[i]
#             print(tickers[i])
#             for k in range(0,len(temp_list)):
#                 longdate = temp_list[k]['date']
#                 date = longdate[0:10]
#                 dict[date] = temp_list[k]['adjClose']  
#             table.append(dict);
#         return table
    
#     def write_csv(table,pricefile):
#         #Write into csv
#         df = pd.DataFrame(table)
#         df.to_csv(pricefile, index=False)
    
    
#     def import_content(pricefile,collection):
#         #import the csv file to MongoDB Atlas
#         client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
#         db = client['MIE479'] # Replace mongo db name
#         collection_name = collection # Replace mongo db collection name
#         db_cm = db[collection_name]
#         cdir = os.path.dirname(__file__)
#         file_res = os.path.join(cdir, pricefile)
    
#         data = pd.read_csv(file_res)
#         data_json = json.loads(data.to_json(orient='records'))
#         db_cm.delete_many({})
#         db_cm.insert_many(data_json)
        
#     def read_data(collection):
#         #read data from Atlas collections
#         client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority")
#         db = client.MIE479
#         cursor = db[collection].find()       
#         df = pd.DataFrame(list(cursor))
#         df = df.drop(['_id'],axis = 1)
        
#         return df
    
#     def save_into_mongo (data, collection):
#         client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority") 
#         db = client.MIE479
#         collection = db[collection]
#         data.reset_index(inplace=True)
#         data_dict = data.to_dict("record")
#         collection.insert_many(data_dict)
    
#     def write_time_series (data,lookback,card,risk_appetite):
#         #save 4*4*3 cumulated returns into database
#         collection = 'timeseries_L'+str(lookback)+'_C'+str(card)+'_R'+str(risk_appetite)
#         print(collection)
#         Database.save_into_mongo(data,collection)
    
#     def clean_col_save (data, collection):
#         client = pymongo.MongoClient("mongodb+srv://admin:admin@mie479.mvqsq.mongodb.net/MIE479?retryWrites=true&w=majority") 
#         db = client.MIE479
#         collection = db[collection]  
#         cursor = collection.count() 
#         if cursor==0: 
#             print("empty collection")
#         else:
#             collection.delete_many({})
#         data.reset_index(inplace=True)
#         data_dict = data.to_dict("record")
#         collection.insert_many(data_dict)        
        
        
    
# ##main function#################################################################
# ##S&P500 stocks
# #pricefile = 'SP500AdjClose.csv' #the file which the adjusted closing price is written into
# #collection = 'SP500AdjClose'  #the file in which the price is stored 
# #tickers = read_tickers(1) #ticker type 1 = s&p500 tickers
# #dates = get_date()
# #table = get_price(tickers,dates)
# #write_csv(table,pricefile)
# #import_content(pricefile,collection)

# ##S&P1500 stocks
# #pricefile = 'SP1500AdjClose.csv' #the file which the adjusted closing price is written into
# #collection = 'SP1500AdjClose'  #the collection in which the price is stored 
# #tickers = read_tickers(2) #ticker type 2 = S&P1500 tickers
# #dates = get_date()
# #table = get_price(tickers,dates)
# #write_csv(table,pricefile)
# #import_content(pricefile,collection)

# ##ETFs
# #pricefile = 'ETFAdjClose.csv' #the file which the adjusted closing price is written into
# #collection = 'ETFAdjClose'  #the collection in which the price is stored 
# #tickers = read_tickers(3) #ticker type 1 = ETF tickers
# #dates = get_date()
# #table = get_price(tickers,dates)
# #write_csv(table,pricefile)
# #import_content(pricefile,collection)
 

