from rest_framework import permissions, generics

from contact import serializers, models


class ContactListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = serializers.ContactSerializer
    queryset = models.Contact.objects.all()


class AboutUsListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    serializer_class = serializers.AboutUsSerializer
    queryset = models.AboutUs.objects.all()
