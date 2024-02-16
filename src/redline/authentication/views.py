from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import JWTOutput, LoginSerializer

User = get_user_model()


class LoginView(APIView):
    @extend_schema(request=LoginSerializer, responses=JWTOutput)
    def post(self, request: Request) -> Response | Exception:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        username = serializer.validated_data.get("username")
        phone_number = serializer.validated_data.get("phone_number")
        password = serializer.validated_data["password"]

        if email and password:
            lookup_field = {"email": email}
        elif phone_number and password:
            lookup_field = {"phone_number": phone_number}
        elif username and password:
            lookup_field = {"username": username}
        else:
            return Response(
                "one of these 3 field is required >>> username,email,phone_number ",
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(**lookup_field)
            if user and user.check_password(password):

                return Response(self.generate_token(user))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed

    def generate_token(self, user: User) -> dict:
        refresh = RefreshToken.for_user(user)

        return JWTOutput({"refresh": refresh, "access": refresh.access_token}).data
