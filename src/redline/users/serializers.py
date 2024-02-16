from attr import fields
from jsonschema import ValidationError
from rest_framework import serializers

from redline.users.utils import User


class UserInput(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=13, required=False)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        super().validate(attrs)
        password1 = attrs.get("password")
        password2 = attrs.get("password_confirm")
        if password1 != password2:
            raise ValidationError("passwords must be the same !!")
        del attrs["password_confirm"]
        return attrs


class UserOutput(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
        )
