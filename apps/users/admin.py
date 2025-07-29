from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import CustomUser
from apps.dashboards.models import WorkSpace

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    ordering = ('email',)