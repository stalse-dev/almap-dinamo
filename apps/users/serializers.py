from rest_framework import serializers

from apps.users.models import CustomUser, Role


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Role model.
    """

    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model with nested roles and groups.
    """

    # roles = RoleSerializer(many=True, read_only=True)
    # custom_groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar_url",
        )
