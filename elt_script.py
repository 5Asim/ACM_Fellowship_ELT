import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import pandas as pd
from io import StringIO

# Load environment variables
load_dotenv()

# Azure Blob service client
connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "fellowshiptask1"  # Replace with your container name

def extract_data():
    try:
        # Extract data from a blob and return as DataFrame
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client("data/raw_data.csv")
        download_stream = blob_client.download_blob()
        df = pd.read_csv(StringIO(download_stream.content_as_text()))
        return df
    except Exception as e:
        print(f"Error in extract_data: {e}")
        raise

def transform_data(df):
    try:
        # Add a new column using the correct column name
        df['processed'] = df['Value'] * 2
        return df
    except Exception as e:
        print(f"Error in transform_data: {e}")
        raise

def load_data(df):
    try:
        # Save transformed data back to blob storage
        output = StringIO()
        df.to_csv(output, index=False)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob="data/transformed_data.csv")
        blob_client.upload_blob(output.getvalue(), overwrite=True)
    except Exception as e:
        print(f"Error in load_data: {e}")
        raise

def run_elt():
    try:
        df = extract_data()
        df_transformed = transform_data(df)
        load_data(df_transformed)
        print("ELT process completed successfully.")
    except Exception as e:
        print(f"ELT process failed: {e}")

if __name__ == "__main__":
    run_elt()
