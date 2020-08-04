from django.urls import path
from hotel import views

urlpatterns = [
    path('domestic-cities/', views.get_domestic_cities),
    path('international-cities/', views.get_international_cities),
    path('hotel/', views.PublicHotelListAPIView.as_view(), name='public-hotel-list'),
    path('hotel/<int:id>', views.PublicHotelRetrieveAPIView.as_view(), name='public-hotel-detail'),
    path('<str:city>/', views.PublicHotelListAPIViewByCity.as_view()),
]
