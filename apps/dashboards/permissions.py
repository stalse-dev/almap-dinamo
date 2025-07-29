from rest_framework.permissions import BasePermission
from apps.dashboards.models import WorkSpace

class CanViewDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard' e que estejam em um Workspace que contenha o dashboard.
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.has_perm('dashboards.view_dashboard')

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == 'Master Admin':
            return True
        return WorkSpace.objects.filter(dashboards=obj, users=user).exists()


class CanEmbedDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard' e que estejam em um Workspace que contenha o dashboard.
    """
    # def has_permission(self, request, view):
    #     user = request.user
        
    #     return user.is_authenticated and user.has_perm('dashboards.view_dashboard')

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated or not user.has_perm('dashboards.view_dashboard'):
            return False
        # obj é o Dashboard
        return WorkSpace.objects.filter(dashboards=obj, users=user).exists()


class CanApproveDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'can_approve_dashboard'.
    """
    def has_permission(self, request, view):
        user = request.user
        # Usuário autenticado e tem permissão direta ou via grupo
        return user.is_authenticated and user.has_perm('dashboards.can_approve_dashboard')
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == 'Master Admin':
            return True
        return WorkSpace.objects.filter(dashboards=obj, users=user).exists()


class CanPublishDashboardPermission(BasePermission):
    """
    Permite acesso apenas a usuários ou grupos com a permissão 'view_dashboard'.
    """
    def has_permission(self, request, view):
        user = request.user
        # Usuário autenticado e tem permissão direta ou via grupo
        return user.is_authenticated and user.has_perm('dashboards.can_publish_dashboard')
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.group and user.group.name == 'Master Admin':
            return True
        return WorkSpace.objects.filter(dashboards=obj, users=user).exists()


