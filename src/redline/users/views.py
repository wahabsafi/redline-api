from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from redline.core.exceptions import ResponseException

from .serializers import UserInput, UserOutput
from .services import UserRegisterInput, create_user


class UserRegister(APIView):
    @extend_schema(request=UserInput, responses=UserOutput)
    def post(self, request: Request) -> Response:
        serializer = UserInput(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            params = UserRegisterInput(**serializer.validated_data)
            user = create_user(params)
            return Response(UserOutput(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                str(ResponseException(e)), status=status.HTTP_400_BAD_REQUEST
            )
