from rest_framework_simplejwt.serializers import \
    TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from user import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add custom claims to jwt token"""
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # add custom claims
        token['username'] = user.username
        token['staff'] = user.is_staff
        token['email'] = user.email
        token['phone'] = user.phone_number
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
    email = serializers.EmailField(required=True)
    address = serializers.CharField()
    state = serializers.CharField()

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'username', 'password', 'email',
                  'phone_number', 'address', 'state')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class EmergencyInfoSerializer(serializers.ModelSerializer):
    '''Emergency Contact details
    '''
    class Meta:
        model = models.EmergencyInfo
        fields = ('tenant', 'name', 'contact_address', 'occupation',
                  'place_of_work', 'phone')


class UserBankInfoSerializer(serializers.ModelSerializer):
    '''User Bank Information'''

    class Meta:
        model = models.UserBankInfo
        fields = ('tenant', 'bank_name', 'account_name', 'account_number')


class UserDetailSerializer(WritableNestedModelSerializer):
    """personal details
    state_of_origin, occupation, place_of_work,
    """
    emergency = EmergencyInfoSerializer(allow_null=True)
    bank_details = UserBankInfoSerializer(many=True, allow_null=True)

    class Meta:
        model = models.User
        fields = ('id', 'state_of_origin', 'occupation', 'place_of_work',
                  'bank_details', 'emergency')
        read_only_fields = ('id',)
