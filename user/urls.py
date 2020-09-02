from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user import views

urlpatterns = [
    path('user/create/', views.UserCreate.as_view(), name='create_user'),
    path(
        'token/obtain/',
        views.ObtainTokenPairWithUsernameView.as_view(),
        name='token_create'
    ),  # override sjwt stock token -> jwt_views.TokenObtainPairView.as_view()
    path('token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('blacklist/',
         views.LogoutAndBlacklistRefreshTokenForUserView.as_view(),
         name='blacklist'),
]
