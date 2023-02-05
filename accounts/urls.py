from django.urls import path
from .views import LoginView,UserVerifyView

app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(), name="user_login"),
    path("login_verify/", UserVerifyView.as_view(), name="user_login_verify"),
]
