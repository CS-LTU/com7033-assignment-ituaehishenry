from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
from bson.objectid import ObjectId

# Connect to MongoDB using the environment variable
client = MongoClient(os.getenv('MONGODB_URI'))
db = client["Stroke_db"]
patient_collection = db["Stroke"]

def add_patient(patient_data):
    """
    Add a new patient record into the collection.
    Return the inserted id.
    """
    try:
        result = patient_collection.insert_one(patient_data)  # Fix: insert actual data
        print(f"Inserted with _id: {result.inserted_id}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    
def view_patient(username=None, is_admin=False):
        """
        retrieve all patient record to the mongoDB collection with RBAC.
        Admin sees all information about patients
        while users(patients) see only their record
        """
        try:
            if is_admin: 
                patients = list(patient_collection.find())
            else:
                 patients = list(patient_collection.find({'created_by':username}))    
            for patient in patients:
                 patient['_id'] = str(patient['_id'])

            return patients
        except Exception as e:
            print(f"Error retrieving patients: {e}")
            return []
            
def update_patient(patient_id,updated_data, username=None, is_admin=False):
     """
     Update_an existing patient record in the mongoDB collection with RBAC
     Admin can update any patient
     users(patient) can only update their records

     """
     try:
          query = {"-id": ObjectId(patient_id)}
          if not is_admin:
               query['created_by'] = username
          result = patient_collection.update_one(query,{"$set": updated_data})
          return True
     except Exception as e:
          print(f"Error updating patient: {e}")
          return False
def delete_patient(patient_id, username, is_admin=False):
          """
          Delete a patient record from the mongoDB collection with RBAC
          Admin can delete any patient record
          Users(patients) can only delete their own record
          """
          try:
               query = {"_id": ObjectId(patient_id)}
               if not is_admin:
                    query['created_by'] = username

               result = patient_collection.delete_one(query)
               return True
          except Exception as e:
               print(f"Error deleting patient: {e}")
               return False

     

