from django.urls import path
from users.views import (
    CreateUserView,
    CookieTokenObtainPairView,
    ManageUserView,
    GenerateTelegramLinkView
)

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CookieTokenObtainPairView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),
    path("telegram-link/", GenerateTelegramLinkView.as_view(), name="telegram_link"),
]

app_name = "users"
