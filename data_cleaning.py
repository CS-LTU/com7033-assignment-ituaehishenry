import pandas as pd
import numpy as np
"""Cleaning the dataset to be ready to be imported into the
  data base and do other analysis """
#Creating a file path# File paths
INPUT_FILE = "Original_healthcare_dataset_stroke_data.csv"
OUTPUT_FILE = "EDA_data.csv"

def load_dataset(file_path):
    """
    Load the dataset from the CSV file .
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Dataset loaded successfully with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except Exception as err:
        print(f"Error loading dataset: {err}")
        return None
def handle_missing_values(data):
    """
    Handle missing values in the dataset.
    Median will be used instead of mean as median 
    gives better reult in the case of outliers
     - Fill missing BMI values with the median.

    """

    if 'bmi' in data.columns:
        missing_bmi = data['bmi'].isnull().sum()
        if missing_bmi > 0:
            median_bmi = data['bmi'].median()
            data['bmi'].fillna(median_bmi, inplace=True)
            print(f"Filled {missing_bmi} missing BMI values with median: {median_bmi:.2f}")
        else:
            print("No missing BMI values found.")
    return data

def clean_data(data):
     """
     Cleaning the dataset and standardizing column names and values.
    - Converting categorical text data to lowercase.
    This is avoid inconsistenccy in dataset.
     """
    
     data['gender'] = data['gender'].str.lower()
     data['ever_married'] = data['ever_married'].str.lower()
     data['work_type'] = data['work_type'].str.lower()
     data['Residence_type'] = data['Residence_type'].str.lower()
     data['smoking_status'] = data['smoking_status'].str.lower()
     print("Data cleaning completed.")
     return data

def save_data(data, file_path):
    """
    
    Save the cleaned dataset to a CSV file.
    """
    try:
        data.to_csv(file_path, index=False)
        print(f"Cleaned data saved to '{file_path}'.")
    except Exception as err:
        print(f"Error saving cleaned data: {err}")

def display_data_summary(data):
    """
   Display basic statistics and a summary of the dataset.
    """
    
    print("\nBasic Statistics:")
    print(data.describe())
    
    print("\nData Info:")
    print(data.info())

    print("\nMissing Values Summary:")
    print(data.isnull().sum())

def main():
    # Step 1: Load the dataset
    data = load_dataset(INPUT_FILE)
    if data is None:
        return

    # Step 2: Handle missing values for analysis
    data = handle_missing_values(data)

    # Step 3: Clean the data
    data = clean_data(data)

    # Step 4: Show data summary
    display_data_summary(data)

    # Step 5: Save the EDA dataset
    save_data(data, OUTPUT_FILE)

if __name__ == "__main__":
    main()