from django.urls import path

from payments import views

urlpatterns = [
    path("payment/",
         views.PaymentListCreateView.as_view(),
         name="create_payment")
]
