from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(max_length=14, required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=True, style={"input_type": "password"})


class JWTOutput(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
