from django.shortcuts import render
from django.http import JsonResponse
from .controller import firebase_handler, trends, news_handler
from files.data_handling_scripts.updateData import updateStockData
from configparser import ConfigParser
from datetime import datetime, timedelta
import os

config = ConfigParser()

# Create your views here.
def home(request):
    stocks_data = trends.get_stock_trend()
    context = {"stocks_data":stocks_data}
    return render(request, "finance/index.html", context=context)

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
