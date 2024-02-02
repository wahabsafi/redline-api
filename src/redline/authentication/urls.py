from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import LoginView
app_name='auth'
urlpatterns = [
        path('jwt/', include(([
            path('login/', LoginView.as_view(),name="login"),
            path('refresh/', TokenRefreshView.as_view(),name="refresh"),
            path('verify/', TokenVerifyView.as_view(),name="verify"),
            ])), name="jwt"),
]