from django.urls import path
from hotel import views

urlpatterns = [
    path('search/', views.hotel_search, name='hotel-search'),
]
