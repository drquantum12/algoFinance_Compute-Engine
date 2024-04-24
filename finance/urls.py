from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('adminPanel/', views.updateRecordPage, name="adminPanel"),
    path('news/', views.news, name="news"),
    path('stock_data/get/', views.stock_data, name="stock_data"),
    path('update_records/', views.updateData, name="update_records"),
    path('update_news_records/', views.update_news_records_on_firestore, name="update_news_records")
]