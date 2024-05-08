from google.cloud import firestore, storage, aiplatform
from datetime import datetime, timedelta


GOOGLE_APPLICATION_CREDENTIALS = "google-credentials.json"

class FirestoreHandler:
    def __init__(self):
        self.db = firestore.Client(project='tradegradient')

    def add_document(self, collection_name, document_name, data):
        self.doc_ref = self.db.collection(collection_name).document(document_name)
        self.doc_ref.set(data)

    def read_collection(self, collection_name):
        self.collection_ref = self.db.collection(collection_name)
        documents = self.collection_ref.stream()
        data = []
        for doc in documents:
            doc_date_str = doc.id
            doc_date = datetime.strptime(doc_date_str, "%d-%m-%Y")
            today = datetime.now().date()
            if today - timedelta(days=3) <= doc_date.date() <= today:
                for news in doc.to_dict()["news"]:
                    data.append(news)
        return data[::-1]

    def read_document(self, collection_name, document_name):
        self.doc_ref = self.db.collection(collection_name).document(document_name)
        return self.doc_ref.get().to_dict()
    
    def update_document(self, collection_name, document_name, data):
        self.doc_ref = self.db.collection(collection_name).document(document_name)
        self.doc_ref.update(data)
    
    def delete_document(self, collection_name, document_name):
        self.doc_ref = self.db.collection(collection_name).document(document_name)
        self.doc_ref.delete()

class CloudStorageHandler:
    def __init__(self):
        self.storage_client = storage.Client(project='tradegradient')

    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        self.bucket = self.storage_client.bucket(bucket_name)
        self.blob = self.bucket.blob(destination_blob_name)
        self.blob.upload_from_filename(source_file_name)

    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        self.bucket = self.storage_client.bucket(bucket_name)
        self.blob = self.bucket.blob(source_blob_name)
        self.blob.download_to_filename(destination_file_name)

    def list_blobs(self, bucket_name):
        self.bucket = self.storage_client.bucket(bucket_name)
        return self.bucket.list_blobs()

    def delete_blob(self, bucket_name, blob_name):
        self.bucket = self.storage_client.bucket(bucket_name)
        self.blob = self.bucket.blob(blob_name)
        self.blob.delete()

