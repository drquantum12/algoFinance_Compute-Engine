from django.shortcuts import render, redirect
from django.http import JsonResponse
from .controller import firebase_handler, trends, news_handler
from files.data_handling_scripts.updateData import updateStockData
from configparser import ConfigParser
from datetime import datetime, timedelta
import os
from kiteconnect import KiteConnect

config = ConfigParser()
config.read("files/configuration.ini")

# Create your views here.
HOST = "127.0.0.1"
PORT = 8000
kite_api_key = config.get("kite", "api_key")
kite_api_secret = config.get("kite", "api_secret")

# Create a redirect url
redirect_url = "http://{host}:{port}/login".format(host=HOST, port=PORT)

# Login url
login_url = "https://kite.zerodha.com/connect/login?api_key={api_key}".format(api_key=kite_api_key)

# Kite connect console url
console_url = "https://developers.kite.trade/apps/{api_key}".format(api_key=kite_api_key)

def get_kite_client(config=config):
    """Returns a kite client object
    """
    access_token = config.get("kite", "access_token")

    kite = KiteConnect(api_key=kite_api_key)
    if access_token:
        kite.set_access_token(access_token=access_token)
    return kite

# currently saving access token in configuration file for single user,
# for multiple users we can save access token in database and fetch it

def login(request):
    request_token = request.GET.get('request_token')
    if not request_token:
        return redirect(login_url)

    kite = get_kite_client()
    data = kite.generate_session(request_token, api_secret=kite_api_secret)
    config.set("kite", "access_token", data["access_token"])
    with open("files/configuration.ini", "w") as file:
        config.write(file)
    return redirect("home")

# Create your views here.
def home(request):
    try:
        kite_client=get_kite_client()
        stocks_data = trends.get_stock_trend(request=request, kite_client=kite_client, duration=30, interval="60minute")
        context = {"stocks_data":stocks_data}
        return render(request, "finance/index.html", context=context)
    except:
        return redirect(login_url)
    

def news(request):
    news = firebase_handler.FirestoreHandler().read_collection("news")
    context = {"news_list":news}
    return render(request, "finance/news.html", context=context)

def stock_data(request):
    if request.method == "POST":
        stock_symbol = request.POST.get("stock_symbol")
        stock_index = request.POST.get("stock_index")
        data = trends.stock_price_data(stock_symbol, stock_index)
        return JsonResponse(data, safe=False)
    
def updateRecordPage(request):
    config.read("files/configuration.ini")
    last_updated = config["status_config"]["last_updated"]
    status = "Records Updated"
    context = {"last_updated":last_updated,
               "status" : status}
    return render(request, "finance/adminPanel.html", context=context)
    
def updateData(request):
    if request.method == "GET":
        updateStockData()
        config.read("files/configuration.ini")
        last_updated = config["status_config"]["last_updated"]
        response = {"last_updated": last_updated}
        return JsonResponse(response, safe=False)
    

def error_404(request, exception):
    return render(request, "finance/404.html")

def update_news_records_on_firestore(request):
    if request.method == "GET":
        storage = firebase_handler.CloudStorageHandler()
        firestore = firebase_handler.FirestoreHandler()
        # extract news
        news = news_handler.extract_news()

        # check all documents in news collection and move to cloud storage if older than 7 days
        documents = firestore.read_collection("news")
        try:
            for doc in documents:
                if datetime.strptime(doc["pubDate"], "%d-%m-%Y") < (datetime.now() - timedelta(days=7)):
                    file_path = "old_record.json"
                    with open(file_path, "w") as f:
                        f.write(doc.to_json())
                    if os.path.exists(file_path):
                        storage.upload_blob("algo_finance_archive_news", file_path, f"{doc['pubDate']}.json")
                        firestore.delete_document("news", doc.id)
        except Exception as e:
            print(e)

                

        # add news to firestore
        date = datetime.now().strftime("%d-%m-%Y")
        record = {"news":news}
        firestore.add_document("news", date, record)

        
        response = {"last_updated": date}
        return JsonResponse(response, safe=False)
