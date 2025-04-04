from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "telegram_chat_id")
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_password(value):
        validate_password(value)
        return value

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
                is_moderator=validated_data.get("is_moderator", False),
                is_manager=validated_data.get("is_manager", False),
                telegram_chat_id=validated_data.get("telegram_chat_id", None)
            )
            return user
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        try:
            instance.save()
        except Exception as e:
            raise serializers.ValidationError({"detail": str(e)})

        return instance
