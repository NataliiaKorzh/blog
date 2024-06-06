from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for custom user model.

    This serializer is used to serialize user data with specified fields.

    """
    class Meta:
        model = User
        fields = ("id", "email", "avatar", "is_staff", "is_active")


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer is used to validate and create a new user instance.

    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("name", "email", "password", "avatar")

    def create(self, validated_data):
        """
        Create a new user instance.

        Args:
            validated_data (dict): The validated data for user creation.

        Returns:
            User: The newly created user instance.
        """
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
            avatar=validated_data.get("avatar"),
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.

    This serializer is used to update user profile information.

    """
    class Meta:
        model = User
        fields = ("name", "email", "avatar")

    def update(self, instance, validated_data):
        """
        Update user profile.

        Args:
            instance (User): The user instance to be updated.
            validated_data (dict): The validated data for user profile update.

        Returns:
            User: The updated user instance.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance
