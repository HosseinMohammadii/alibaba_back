from django.urls import path
from hotel import views

urlpatterns = [
    path('domestic-cities/', views.get_domestic_cities),
    path('international-cities/', views.get_international_cities),
    path('hotels/', views.PublicHotelListAPIView.as_view(), name='public-hotel-list'),
    path('hotels/<int:id>', views.PublicHotelRetrieveAPIView, name='public-hotel-detail'),
]
