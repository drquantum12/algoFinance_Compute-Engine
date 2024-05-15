from django.shortcuts import render, redirect
from django.http import JsonResponse
from .controller import firebase_handler, trends, news_handler
from files.data_handling_scripts.updateData import updateStockData
from configparser import ConfigParser
from datetime import datetime, timedelta
import os
import json

config = ConfigParser()
config.read("files/configuration.ini")







# currently saving access token in configuration file for single user,
# for multiple users we can save access token in database and fetch it



# Create your views here.
def home(request):
    with open("stocks.json", "r") as file:
            stocks_data = list(json.load(file).items())
    news_list = firebase_handler.FirestoreHandler().read_collection("news")

    # sector_wise_sentiments = {'Banking': {'Positive': 1}, 'Auto': {'Positive': 1}, 'FMCG': {'Negative': 2, 'Positive': 2, 'Neutral': 1}, 'Energy': {}, 'Industrial': {'Positive': 1}, 'Healthcare': {'Neutral': 2}, 'Services': {'Negative': 2, 'Neutral': 4, 'Positive': 2}, 'Media': {}, 'Transportation': {'Negative': 1, 'Neutral': 1}, 'Tech': {'Positive': 2, 'Negative': 1, 'Neutral': 1}, 'Telecom': {'Positive': 1}}
    sector_wise_sentiments = {
        "Banking": {},
        "Auto": {},
        "FMCG": {},
        "Energy": {},
        "Industrial": {},
        "Healthcare": {},
        "Services": {},
        "Media": {},
        "Transportation": {},
        "Tech": {},
        "Telecom": {}
    }
    for news in news_list:
        if news["sentiment"] == "Positive":
            sector_wise_sentiments[news["tag"]]["Positive"] = sector_wise_sentiments[news["tag"]].get("Positive", 0) + 1
        elif news["sentiment"] == "Negative":
            sector_wise_sentiments[news["tag"]]["Negative"] = sector_wise_sentiments[news["tag"]].get("Negative", 0) + 1
        else:
            sector_wise_sentiments[news["tag"]]["Neutral"] = sector_wise_sentiments[news["tag"]].get("Neutral", 0) + 1
    

    context = {
        "stocks_data":stocks_data,
        "sector_wise_sentiments": sector_wise_sentiments,
        }

    return render(request, "finance/index.html", context=context)

# for route news/<news_type:str>/, news_type is a string
def news(request, news_type=None):
    news = firebase_handler.FirestoreHandler().read_collection("news")
    if news_type == None:
        context = {"news_list":news}
        return render(request, "finance/news.html", context=context)
    else:
        news_list = []
        for news_item in news:
            if news_item["tag"] == news_type:
                news_list.append(news_item)
        context = {"news_list":news_list}
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
