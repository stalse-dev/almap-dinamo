from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from apps.users.models import CustomUser, Role
from apps.dashboards.models import GroupDashboard


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    ordering = ("email",)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    ordering = ("name",)
    filter_horizontal = ("permissions",)


admin.site.unregister(Group)
