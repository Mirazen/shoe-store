from django.urls import path, include
from . import views
from .views import RegisterView

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("guest/", views.guest_login, name="guest"),
    path("profile/", views.profile, name="profile"),
    path("registration/", RegisterView.as_view(), name="register"),
]
