from django.contrib import admin
from django.urls import path,include

app_name='api'

urlpatterns = [
    path('auth/',include('redline.authentication.urls','auth'))
]
