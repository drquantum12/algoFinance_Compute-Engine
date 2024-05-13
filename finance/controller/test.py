from firebase_handler import FirestoreHandler, CloudStorageHandler



if __name__ == "__main__":
    firestore_client = FirestoreHandler()
    news_list = firestore_client.read_collection("news")
    # dictionary to store sector wise sentiments with keys Banking/Finance, Auto, Consumer Products,
              #   Energy ,Industrial Goods and Services, Healthcare and Biotech,
              # Services, Media/Entertainment, Transportation, Tech, Telecom

    sector_wise_sentiments = {
        "Banking/Finance": {},
        "Auto": {},
        "Consumer Products": {},
        "Energy": {},
        "Industrial Goods and Services": {},
        "Healthcare and Biotech": {},
        "Services": {},
        "Media/Entertainment": {},
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
    print(sector_wise_sentiments)



