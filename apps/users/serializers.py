from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from apps.users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for CustomUser model.
    """
    class Meta:
        model = CustomUser
        fields = '__all__'
    

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group model.
    """
    class Meta:
        model = Group
        fields = '__all__'
        
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
