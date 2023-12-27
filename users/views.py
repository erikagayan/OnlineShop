from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserSerializer
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
