from django.urls import path
from rest_framework_simplejwt import views as jwt_views

# from rest_framework.routers import DefaultRouter

from user import views

# router = DefaultRouter()
# router.register('users', views.ListUsers, basename='user')

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
    path('user/update/<int:id>/',
         views.UpdateUserDetail.as_view(), name='update_user'),
]

# urlpatterns += router.urls
