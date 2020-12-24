from rest_framework import permissions, generics

from payments import serializers, models


class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()
    """
        List and Create payment instances for users
    """
    serializer_class = serializers.PaymentSerializer
    queryset = models.Payment.objects.all()
    # @TODO ensure only staff's can list payments
    # def get_queryset(self):
