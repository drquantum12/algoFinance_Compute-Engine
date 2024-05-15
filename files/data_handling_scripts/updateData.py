import pandas as pd
import yfinance
import os
import re
from configparser import ConfigParser
from datetime import datetime
from kiteconnect import KiteConnect

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
config = ConfigParser()
config.read("files/configuration.ini")

# Create your views here.
kite_api_key = config.get("kite", "api_key")
kite_api_secret = config.get("kite", "api_secret")

# Login url
login_url = "https://kite.zerodha.com/connect/login?api_key={api_key}".format(api_key=kite_api_key)

# Kite connect console url
console_url = "https://developers.kite.trade/apps/{api_key}".format(api_key=kite_api_key)

config = ConfigParser()
config.read("files/configuration.ini")

# def login(request):
#     request_token = request.GET.get('request_token')
#     if not request_token:
#         return redirect(login_url)
    
#     config.set("kite","request_token",request_token)
#     with open("files/configuration.ini", "w") as file:
#         config.write(file)

#     kite = KiteConnect(api_key=kite_api_key)
#     data = kite.generate_session(request_token, api_secret=kite_api_secret)
#     kite.set_access_token(data["access_token"])
#     config.set("kite", "access_token", data["access_token"])
#     with open("files/configuration.ini", "w") as file:
#         config.write(file)
#     return redirect("home")

def get_kite_client(config=config):
    """Returns a kite client object
    """
    access_token = config.get("kite", "access_token")

    kite = KiteConnect(api_key=kite_api_key)
    if access_token:
        kite.set_access_token(access_token=access_token)
    return kite

def updateStockData():
        
        with open("files/configuration.ini", "w") as configFile:
             config.set("status_config","last_updated", datetime.today().strftime("%d-%m-%Y"))
             config.write(configFile)

if __name__ == "__main__":
    updateStockData(config=config)