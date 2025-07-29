from django.conf import settings
from django.db import models
from auditlog.registry import auditlog

class Dashboard(models.Model):
    title = models.CharField(max_length=200)
    embed_url = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_dashboards"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_dashboards"
    )


    published = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        permissions = [
            ("can_approve_dashboard", "Can approve dashboard"),
            ("can_publish_dashboard", "Can publish dashboard"),
            ("can_view_global_dashboard", "Can view dashboards globally"),
        ]

    def __str__(self):
        return self.title


class WorkSpace(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)
    dashboards = models.ManyToManyField(
        Dashboard,
        related_name="dashboard_groups",
        blank=True,
        null=True
    )
    
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dashboard_workspaces",
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_dashboard_groups"
    )
    
    def __str__(self):
        return f"{self.name} - {self.description}"


auditlog.register(Dashboard)
auditlog.register(WorkSpace)