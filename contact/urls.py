from django.urls import path

from contact import views

urlpatterns = [
    path("contact/",
         views.ContactListView.as_view(),
         name="get_contacts"),
    path("about/", views.AboutUsListView.as_view(), name="get_about")
]
