import pandas as pd
import yfinance
import os
import re
from configparser import ConfigParser
from datetime import datetime

# from google.cloud import storage
# from django.conf import settings

# GOOGLE_CLOUD_STORAGE_BUCKET_NAME = 'drquantum_stock_files'
# GOOGLE_APPLICATION_CREDENTIALS = os.path.abspath('files/keyfile.json')

# def fetch_records(object_name = "indices"):
#     settings.configure()
#     bucket_name = GOOGLE_CLOUD_STORAGE_BUCKET_NAME
#     storage_client = storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
#     bucket = storage_client.bucket(bucket_name=bucket_name)

#     objects = bucket.list_blobs(prefix=object_name)
#     return objects

indices_files = [file for file in os.listdir("files/indices") if not file.startswith(".")]

config = ConfigParser()
config.read("files/configuration.ini")

def updateStockData():
        for index in indices_files:
            try:
                index_folder_name = index.replace(".csv","")
                pattern = r'ind_|_?list'
                index_folder_name = re.sub(pattern, "", index_folder_name).replace("nifty","nifty ").capitalize()
                os.makedirs(f"files/indices_stock_data/{index_folder_name}", exist_ok=True)

                df_index = pd.read_csv(f"files/indices/{index}")

                for symbol in df_index.Symbol.values:
                    stock_name = f"{symbol}.NS"
                    stock = yfinance.Ticker(stock_name).history(period="60d", interval="1d")[["Close", "Volume"]]
                    stock.to_csv(f"files/indices_stock_data/{index_folder_name}/{stock_name}.csv")
            except Exception as e:
                print(e)
        with open("files/configuration.ini", "w") as configFile:
             config.set("status_config","last_updated", datetime.today().strftime("%d-%m-%Y"))
             config.write(configFile)

if __name__ == "__main__":
    updateStockData(config=config)