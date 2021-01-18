from django.urls import path

from notification import views

urlpatterns = [
    path("notification/",
         views.NotificationListCreateView.as_view(),
         name="get_notification")
]
