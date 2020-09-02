from rest_framework_simplejwt.serializers import \
    TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from user import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add custom claims to jwt token"""
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # add custom claims
        token['username'] = user.username
        token['staff'] = user.is_staff
        return token


class UserSerializer(serializers.ModelSerializer):
    """Currently unused in preference of the below"""
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(validators=[
        UniqueValidator(queryset=models.User.objects.all(),
                        message="This username already exist!")
    ])
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'password',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
