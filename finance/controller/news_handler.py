import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime
from finance.ml_models import sentiment

urls = [
    "https://economictimes.indiatimes.com/markets/stocks/news",
]


def extract_news():
    s= sentiment.Sentiment()
    all_news = []
    response = requests.get(urls[0])
    soup = BeautifulSoup(response.text, "html.parser")
    news_records = soup.find_all("div", class_="eachStory")
    for news in news_records:
        title = news.find("h3").text
        if title not in all_news:
            date = "".join(news.select(".date-format")[0].text.split(",")[:2])
            pubDate = datetime.strptime(date,"%b %d %Y").strftime("%d-%m-%Y")
            if pubDate == datetime.now().strftime("%d-%m-%Y"):
                para = news.find("p").text
                sntmt = s.get_sentiment(para)
                all_news.append(
                    {"title": title,
                    "pubDate": pubDate,
                        "para": para,
                        "sentiment": sntmt})
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

