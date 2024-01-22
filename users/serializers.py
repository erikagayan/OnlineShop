from rest_framework import serializers
from django.contrib.auth import get_user_model
from .validators import CustomPasswordValidator


class UserSerializer(serializers.ModelSerializer):
    password_validator = CustomPasswordValidator()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        # Use our custom validator to validate the password
        errors = self.password_validator.validate_password(value)
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
