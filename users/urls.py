from django.urls import path
from users.views import CreateUserView, CookieTokenObtainPairView, ManageUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("login/", CookieTokenObtainPairView.as_view(), name="token"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "users"
