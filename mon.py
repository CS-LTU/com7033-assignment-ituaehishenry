import pymongo
print(pymongo.__version__)

from pymongo import MongoClient
#Connect to tjhe mongoDFB server
client = MongoClient('mongodb+srv://ituaehishenry:West8coast@cluster0.mqgy9ii.mongodb.net/')

# Get the server information
server_info = client.server_info()

#Extracting and printing the MongoDB version
mongo_version = server_info['version']
print(f'MongoDB Version: {mongo_version}')
from pymongo import MongoClient
import pandas as pd

client = MongoClient('mongodb+srv://ituaehishenry:West8coast@cluster0.mqgy9ii.mongodb.net/?appName=Cluster0')
db = client['World']
collection = db['city']

cursor = collection.find()
collection.find({"country":"UK"})
data_list = list(cursor)
df = pd.DataFrame(data_list)
print(df.head())
print(df.describe())
df = ['Population'].mean()
for document in data_list:
    print(document)
    

