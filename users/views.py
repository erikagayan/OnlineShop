import uuid
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import TelegramToken
from users.serializers import UserSerializer
from users.auth import CookieJWTAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        response = JsonResponse(
            {
                "refresh": str(refresh),
                "access": str(access),
            }
        )

        response.set_cookie(
            key="access",
            value=str(access),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=24 * 60 * 60,
        )
        response.set_cookie(
            key="refresh",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3 * 24 * 60 * 60,
        )

        return response


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (CookieJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    # return auth user
    def get_object(self):
        return self.request.user


class GenerateTelegramLinkView(APIView):
    authentication_classes = (CookieJWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = str(uuid.uuid4())
        telegram_token = TelegramToken.objects.create(user=request.user, token=token)
        bot_username = "online_shop_django_bot"
        telegram_link = f"https://t.me/{bot_username}?start={token}"
        return Response({"telegram_link": telegram_link})
