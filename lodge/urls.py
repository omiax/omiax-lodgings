from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lodge import views

router = DefaultRouter()
router.register('lodges', views.LodgeViewSet)
router.register('rooms', views.RoomViewSet, basename="rooms")

app_name = 'lodge'

urlpatterns = [path('', include(router.urls))]
