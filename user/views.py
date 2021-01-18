from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status, generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from user import serializers

from django.contrib.auth import get_user_model
User = get_user_model()


class ObtainTokenPairWithUsernameView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.MyTokenObtainPairSerializer


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request, format="json"):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UpdateUserDetail(CreateModelMixin, generics.RetrieveUpdateAPIView):
    # permission_classes = (permissions.AllowAny, )
    # authentication_classes = ()

    """
        A viewset for viewing and editing user instances.
    """
    serializer_class = serializers.UserDetailSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
