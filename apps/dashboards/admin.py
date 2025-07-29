from django.contrib import admin
from apps.dashboards.models import Dashboard, GroupDashboard

# Register your models here.


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("title", "created_by", "created_at")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("approved_at",)


@admin.register(GroupDashboard)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    filter_horizontal = ("dashboards", "users")
