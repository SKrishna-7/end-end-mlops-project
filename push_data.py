import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging



load_dotenv()

MONGODB_URL=os.getenv('MONGO_DB_URL')

print(MONGODB_URL)

ca=certifi.where()


class DataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)

            records=list(json.loads(data.T.to_json()).values())

            return records
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def insert_data_db(self,records,db,collection):
        try:
            self.db=db
            self.collection=collection
            self.records=records

            self.mongoclient=pymongo.MongoClient(MONGODB_URL)

            self.db=self.mongoclient[self.db]

            self.collection=self.db[self.collection]

            self.collection.insert_many(self.records)
            
            return len(self.records)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ =='__main__':
    FILE_PATH='Network_Data\phisingData.csv'

    DATABASE="KRISHNA"
    Collection="NetworkData"

    networkobj=DataExtract()
    rec=networkobj.csv_to_json(file_path=FILE_PATH)
    print(rec)

    no_of_rec=networkobj.insert_data_db(records=rec,db=DATABASE,collection=Collection)
    print(no_of_rec)