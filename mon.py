import pymongo
print(pymongo.__version__)

from pymongo import MongoClient
#Connect to the mongoDFB server
client = MongoClient('mongodb+srv://ituaehishenry:West8coast@cluster0.mqgy9ii.mongodb.net/')

# Get the server information
server_info = client.server_info()

#Extracting and printing the MongoDB version
mongo_version = server_info['version']
print(f'MongoDB Version: {mongo_version}')
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId
client = MongoClient('mongodb+srv://ituaehishenry:West8coast@cluster0.mqgy9ii.mongodb.net/?appName=Cluster0')
db = client['World']
collection = db['city']

cursor = collection.find()
collection.find({"country":"UK"})
data_list = list(cursor)
df = pd.DataFrame(data_list)
print(df.head())
print(df.describe())
#df['Population'].mean()

for document in data_list:
    print(document)

    #Helper: pretty  print collection
def show_collection():
     """ Fetch all documents from collection 
     and display them as a Dataframe."""  
     cursor = collection.find() #get all docs
     data_list = list(cursor) #turn into python list
     if not data_list:
          print("\[info] collection is empty.\n")
          return
     df =pd.DataFrame(data_list)
     print("\n==== current document in 'city' collection====")
     print(df)
     print("================================================\n")

#Create
def create_city(name, country, population):
     """
     insert (CREATE) a new city document into cpollectin.
     Returns the inserted"""
     new_doc = {
          "name": name,
          "country": country,
          "population":population
     }
     result = collection.insert_one(new_doc)
     print(f"[CREATE] Inserted document with _id ={result.inserted_id} ")
     return result.inserted_id
#============
# Read
#============
def read_cities(filter_query=None):
     """
     Read (READ) documents from the collection using an optional filter.
       If no filter is provided, return all documents.
       """
     if filter_query is None:
          filter_query = {}
          cursor = collection.find(filter_query)
          docs = list(cursor)
          print (f"[READ] found {len(docs)} document(s) matching {filter_query}:")
          for d in docs:
               print(d)
          return docs 
#=======
# Update
#========
def update_city(document_id, new_population=None, new_name=None):
     """"
     Update (UPDATE) a document by its _id.
     You can change its population and/or name.
     """
     update_field = {}
     update_fields ["population"] = new_population
     if new_name is not None:
          update_fields["name"] = new_name 
          if not update_fields:
               print ("[UPDATE] Nothing to update.") 
               return
          result = collection.update_one(
               {"_id": ObjectId(document_id)}, # which document
               {"$": update_fields}  #how to update
          )      
          print(f"[UPDATE]Matched{result.matched_count},Modifield {result.modified_count}")  

        #======
        # Delete
        # ====== 
     def delete_city(document_id):
          """
            Delete (DELETE) a document by its _id.
            """
          result = collection.delete_one({"_id": ObjectId(document_id)})
          print(f"[DELETE] Delete {result.deleted_count} document(s) with _id ={document_id}")
