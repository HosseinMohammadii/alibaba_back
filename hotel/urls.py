from django.urls import path
from hotel import views

urlpatterns = [
    path('hotels/', views.PublicHotelListAPIView.as_view(), name='public-hotel-list'),
    path('hotels/<int:id>', views.PublicHotelRetrieveAPIView, name='public-hotel-detail'),
]
