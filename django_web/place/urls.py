from django.contrib import admin
from django.urls import path
from . import views

app_name = 'place'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.place_search_list_view, name='search-list'),
    path('place/lists/', views.place_search_list_view, name='place-list'), # 플레이스 리스트
    path('place/detail/<int:store_id>/', views.PlaceDetailView.as_view(), name='place-detail'),
]