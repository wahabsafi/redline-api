from django.contrib import admin
from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("auth/", include("redline.authentication.urls", "auth")),
    path("", include("redline.users.urls", "user")),
]
