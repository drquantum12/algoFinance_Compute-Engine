# from google.cloud import firestore
# from .ml_models import sentiment

# GOOGLE_APPLICATION_CREDENTIALS = "firebase_key.json"

# if __name__ == "__main__":
#     firestore_client = firestore.Client(project='algofinance-419516')
#     collection_ref = firestore_client.db.collection("news")
#     documents = collection_ref.stream()
#     for doc in documents:
#         sentiment_score = sentiment.get_sentiment(doc.to_dict()["para"])
#         doc.update({"sentiment": sentiment_score})
        
