from django.urls import path
from customAuth import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('jwt/token/', views.AuthView.as_view()),
    # path('jwt/token/refresh/', refresh_jwt_token),
    path('jwt/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('jwt/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.UserCreateAPIView.as_view(), name='signup'),
]
