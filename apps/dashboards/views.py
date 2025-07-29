import os
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    DjangoObjectPermissions,
    DjangoModelPermissions,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.dashboards.models import Dashboard, GroupDashboard, DashboardStatus
from apps.dashboards.utils import get_embed_metabase_url, get_embedded_url
from apps.dashboards.serializers import (
    DashboardListSerializer,
    DashboardSerializer,
    GroupDashboardSerializer,
    GroupDashboardRetrieveSerializer,
    GroupDashboardUpdateSerializer,
)
from apps.dashboards.permissions import (
    CanViewDashboardPermission,
    CanApproveDashboardPermission,
    CanPublishDashboardPermission,
    CanEmbedDashboardPermission,
    CanChangeGroupDashboardPermission,
)


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_serializer_class(self):
        if self.action == "create":
            from apps.dashboards.serializers import DashboardCreateSerializer

            return DashboardCreateSerializer
        elif self.action == "list":
            from apps.dashboards.serializers import DashboardListSerializer

            return DashboardListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        group_dashboard_id = self.request.data.get("group_dashboard_id")
        if not group_dashboard_id:
            raise PermissionDenied("group_dashboard_id is required.")
        try:
            group_dashboard = GroupDashboard.objects.get(id=group_dashboard_id)
        except GroupDashboard.DoesNotExist:
            raise PermissionDenied("GroupDashboard not found.")

        if "group_dashboard_id" in serializer.validated_data:
            serializer.validated_data.pop("group_dashboard_id")
        dashboard = serializer.save(created_by=self.request.user)
        group_dashboard.dashboards.add(dashboard)
        group_dashboard.save()

    def get_queryset(self):
        # Detecta se está sendo executado durante a geração do schema
        if getattr(self, "swagger_fake_view", False):
            return Dashboard.objects.none()

        user = self.request.user

        # Verifica se o usuário está autenticado
        if not user.is_authenticated:
            return Dashboard.objects.none()

        is_viewer = user.groups.filter(name="Viewer").exists()
        # Se for apenas viewer, mostra só publicados
        if is_viewer and user.groups.count() == 1:
            return Dashboard.objects.filter(
                dashboard_groups__users=user, status=DashboardStatus.PUBLISHED
            ).distinct()
        # Se for viewer e gestor de área (ou outros grupos), mostra publicados e sandbox
        return Dashboard.objects.filter(
            dashboard_groups__users=user,
            status__in=[DashboardStatus.PUBLISHED, DashboardStatus.SANDBOX],
        ).distinct()


class GroupDashboardViewSet(viewsets.ModelViewSet):
    queryset = GroupDashboard.objects.all()
    serializer_class = GroupDashboardSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "list":
            permission_classes = [IsAuthenticated, DjangoObjectPermissions]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, CanChangeGroupDashboardPermission]
        else:
            permission_classes = [
                IsAuthenticated,
                DjangoModelPermissions,
                DjangoObjectPermissions,
            ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            from .serializers import GroupDashboardCreateSerializer

            return GroupDashboardCreateSerializer
        elif self.action == "retrieve":

            return GroupDashboardRetrieveSerializer

        elif self.action in ["update", "partial_update"]:

            return GroupDashboardUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        group_dashboard = serializer.instance
        group_dashboard.users.add(self.request.user)
        group_dashboard.save()

    def get_queryset(self):
        # Detecta se está sendo executado durante a geração do schema
        if getattr(self, "swagger_fake_view", False):
            return GroupDashboard.objects.none()

        user = self.request.user

        # Verifica se o usuário está autenticado
        if not user.is_authenticated:
            return GroupDashboard.objects.none()

        # Para o método list, filtra os GroupDashboard em que o usuário faz parte
        if self.action == "list":
            return GroupDashboard.objects.filter(users=user)
        if self.action == "retrieve":
            group_dashboard_id = self.kwargs.get("pk")
            return GroupDashboard.objects.filter(id=group_dashboard_id, users=user)
        return super().get_queryset()


class ApproveDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanApproveDashboardPermission]

    def post(self, request, *args, **kwargs):
        """
        Aprova e publica um dashboard.
        Permissões necessárias: can_approve_dashboard
        """
        try:
            dashboard_id = kwargs.get("dashboard_id")
            dashboard = Dashboard.objects.get(id=dashboard_id)
            if not request.user.has_perm("dashboards.can_approve_dashboard"):
                raise PermissionDenied(
                    "You do not have permission to approve this dashboard."
                )

            dashboard.approved_by = request.user
            dashboard.approved_at = timezone.now()
            dashboard.status = DashboardStatus.PUBLISHED
            dashboard.save()

            return Response(
                {"message": "Dashboard approved successfully."},
                status=status.HTTP_200_OK,
            )
        except Dashboard.DoesNotExist:
            raise PermissionDenied(
                "Dashboard not found or you do not have permission to approve it."
            )


class EmbedStaticDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanEmbedDashboardPermission]

    def get(self, request, *args, **kwargs):
        try:
            dashboard_id = kwargs.get("dashboard_id")
            dashboard = Dashboard.objects.get(id=dashboard_id)
            self.check_object_permissions(request, dashboard)
            return Response(
                {"embed_url": get_embedded_url(dashboard_id, request)},
                status=status.HTTP_200_OK,
            )
        except Dashboard.DoesNotExist:
            raise PermissionDenied(
                "Dashboard not found or you do not have permission to view it."
            )


class EmebedSDKDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanViewDashboardPermission]

    def get(self, request, *args, **kwargs):
        try:
            dashboard_id = kwargs.get("dashboard_id")
            dashboard = Dashboard.objects.get(id=dashboard_id)

            if not request.user.has_perm("dashboards.view_dashboard"):
                raise PermissionDenied(
                    "You do not have permission to view this dashboard."
                )

            embed_url = get_embed_metabase_url(dashboard_id, request)
            return render(request, "embed_sdk_dashboard.html", {"embed_url": embed_url})
        except Dashboard.DoesNotExist:
            raise PermissionDenied(
                "Dashboard not found or you do not have permission to view it."
            )


class AccessibleDashboardsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Aplica as mesmas regras do DashboardViewSet
        is_viewer = user.groups.filter(name="Viewer").exists()
        if is_viewer and user.groups.count() == 1:
            dashboards = Dashboard.objects.filter(
                dashboard_groups__users=user, status=DashboardStatus.PUBLISHED
            ).distinct()
        else:
            dashboards = Dashboard.objects.filter(
                dashboard_groups__users=user,
                status__in=[DashboardStatus.PUBLISHED, DashboardStatus.SANDBOX],
            ).distinct()

        data = []
        for dashboard in dashboards:
            group = dashboard.dashboard_groups.first()
            users_count = (
                GroupDashboard.objects.filter(dashboards=dashboard).aggregate(
                    total=Count("users")
                )["total"]
            ) or 0

            data.append(
                {
                    "title": dashboard.title,
                    "description": dashboard.description,
                    "embed_url": dashboard.embed_url,
                    "created_at": dashboard.created_at,
                    "group_dashboard": group.id if group else None,
                    "status": dashboard.status,
                    "users": users_count,
                    "owner": (
                        dashboard.created_by.username if dashboard.created_by else None
                    ),
                }
            )

        return Response(data)
