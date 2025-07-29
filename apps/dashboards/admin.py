from django.contrib import admin
from apps.dashboards.models import Dashboard, WorkSpace

# Register your models here.

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'published', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('published', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('approved_at',)
    
@admin.register(WorkSpace)
class WorkSpaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    filter_horizontal = ('dashboards', 'users')
    