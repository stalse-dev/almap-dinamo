from rest_framework.permissions import BasePermission
from apps.dashboards.models import GroupDashboard


class CanViewDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard' e que estejam em um GroupDashboard que contenha o dashboard.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == "Master Admin":
            return True
        return GroupDashboard.objects.filter(dashboards=obj, users=user).exists()


class CanEmbedDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard' e que estejam em um GroupDashboard que contenha o dashboard.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated or not user.has_perm("dashboards.view_dashboard"):
            return False
        # obj é o Dashboard
        return GroupDashboard.objects.filter(dashboards=obj, users=user).exists()


class CanApproveDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'can_approve_dashboard'.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == "Master Admin":
            return True
        if not user.is_authenticated or not user.has_perm(
            "dashboards.can_approve_dashboard"
        ):
            return False
        return (
            GroupDashboard.objects.filter(dashboards=obj, users=user)
            .exclude(created_by=user)
            .exists()
        )


class CanPublishDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard'.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == "Master Admin":
            return True
        if not user.is_authenticated or not user.has_perm(
            "dashboards.can_publish_dashboard"
        ):
            return False
        return GroupDashboard.objects.filter(dashboards=obj, users=user).exists()


class CanChangeGroupDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'change_groupdashboard'.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.groups and user.groups.name == "Master Admin":
            return True
        if not user.is_authenticated or not user.has_perm(
            "dashboards.change_groupdashboard"
        ):
            return False
        return GroupDashboard.objects.filter(id=obj.id, users=user).exists()
