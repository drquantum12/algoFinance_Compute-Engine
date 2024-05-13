import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from finance.ml_models import sentiment

urls = {
    "Banking" : "https://economictimes.indiatimes.com/industry/banking/finance",
    "Auto" : "https://economictimes.indiatimes.com/industry/auto",
    "FMCG" : "https://economictimes.indiatimes.com/industry/cons-products",
    "Energy" : "https://economictimes.indiatimes.com/industry/energy",
    "Industrial" : "https://economictimes.indiatimes.com/industry/indl-goods/svs",
    "Healthcare" : "https://economictimes.indiatimes.com/industry/healthcare/biotech",
    "Services" : "https://economictimes.indiatimes.com/industry/services",
    "Media" : "https://economictimes.indiatimes.com/industry/media/entertainment",
    "Transportation" : "https://economictimes.indiatimes.com/industry/transportation",
    "Tech" : "https://economictimes.indiatimes.com/tech",
    "Telecom" : "https://economictimes.indiatimes.com/industry/telecom"
}


def extract_news():
    s= sentiment.Sentiment()
    all_news = list()
    for url in urls.items():
        response = requests.get(url[1])
        soup = BeautifulSoup(response.text, "html.parser")
        if url[0] == "Tech":
            news_records = soup.select("#pageContent")[0].select(".top-stories")[0].select(".rList")
            for news in news_records:
                title = news.find("h4").find("a").text
                date = "".join(news.find("time")["data-time"].split(",")[:2])
                pubDate = datetime.strptime(date,"%b %d %Y").strftime("%d-%m-%Y")
                sentiment_score = s.get_sentiment(title)
                if pubDate == datetime.now().strftime("%d-%m-%Y"):
                    all_news.append(
                                    {"title": title,
                                     "tag": url[0],
                                     "sentiment": sentiment_score,
                                    "pubDate": pubDate})
        else:
            news_records = soup.select("#pageContent")[0].select(".top-news")[0].find_all("li")
        
            for news in news_records:
                title = news.find("a").text
                date = "".join(news.select(".date-format")[0].text.split(",")[:2])
                pubDate = datetime.strptime(date,"%b %d %Y").strftime("%d-%m-%Y")
                sentiment_score = s.get_sentiment(title)
                if pubDate == datetime.now().strftime("%d-%m-%Y"):
                    all_news.append(
                                    {"title": title,
                                        "tag": url[0],
                                     "sentiment": sentiment_score,
                                    "pubDate": pubDate})
    return all_news
        


# from lxml import etree

# def extract_news():
#     all_news = []
#     url = 'https://www.moneycontrol.com/rss/economy.xml'
#     response = requests.get(url)
#     tree = etree.fromstring(response.text.encode("utf-8"))
#     channel = tree.find("channel")
#     items = channel.findall("item")
#     for item in items:
#         # extracting unique news title
#         title = re.sub(r'[^a-zA-Z0-9\s+\/]', '', item.find("title").text)
#         if title not in all_news:
#             all_news.append(title)
#     return all_news

