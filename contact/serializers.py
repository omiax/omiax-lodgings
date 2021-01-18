from rest_framework import serializers

from contact.models import Contact, AboutUs, PhoneNumber, EmailAddress


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ('phone', )


class EmailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ('email', )


class ContactSerializer(serializers.ModelSerializer):
    contact_phone = PhoneNumberSerializer(read_only=True, many=True, allow_null=True)
    contact_email = EmailAddressSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = Contact
        fields = ['id', 'location', 'address', 'contact_phone', 'contact_email']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"
