from rest_framework import permissions, generics

from payments import serializers, models


class PaymentListCreateView(generics.ListCreateAPIView):
    # permission_classes = (permissions.AllowAny, )
    # authentication_classes = ()
    """
        List and Create payment instances for users
    """
    serializer_class = serializers.PaymentSerializer

    # ensure only staff's can list all payments
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return models.Payment.objects.all()
        else:
            return models.Payment.objects.filter(tenant=user)
