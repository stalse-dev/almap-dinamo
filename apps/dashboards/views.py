import os
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions, DjangoModelPermissions, BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.dashboards.models import Dashboard, WorkSpace
from apps.dashboards.utils import get_embed_metabase_url
from apps.dashboards.serializers import DashboardSerializer, WorkSpaceSerializer
from apps.dashboards.permissions import CanViewDashboardPermission, CanApproveDashboardPermission, CanPublishDashboardPermission, CanEmbedDashboardPermission
from datetime import datetime


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_serializer_class(self):
        if self.action == 'create':
            from .serializers import DashboardCreateSerializer
            return DashboardCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    


class WorkSpaceViewSet(viewsets.ModelViewSet):
    queryset = WorkSpace.objects.all()
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def get_serializer_class(self):
        if self.action == 'create':
            from .serializers import WorkSpaceCreateSerializer
            return WorkSpaceCreateSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        workspace = serializer.instance
        workspace.users.add(self.request.user)
        workspace.save()


class ApproveDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanApproveDashboardPermission]

    def post(self, request, *args, **kwargs):
        try:
            dashboard_id = kwargs.get('dashboard_id')
            dashboard = Dashboard.objects.get(id=dashboard_id)
            if not request.user.has_perm('dashboards.can_approve_dashboard'):
                raise PermissionDenied("You do not have permission to approve this dashboard.")
            
            dashboard.approved_by = request.user
            dashboard.approved_at = datetime.now()
            dashboard.save()
            
            return Response({"message": "Dashboard approved successfully."}, status=status.HTTP_200_OK)
        except Dashboard.DoesNotExist:
            raise PermissionDenied("Dashboard not found or you do not have permission to approve it.")


class PublishDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanPublishDashboardPermission]
    
    def post(self, request, *args, **kwargs):
        try:
            dashboard_id = kwargs.get('dashboard_id')
            dashboard = Dashboard.objects.get(id=dashboard_id)
            if not request.user.has_perm('dashboards.can_publish_dashboard'):	
                raise PermissionDenied("You do not have permission to publish this dashboard.")
            dashboard.published = True
            dashboard.save()
                  
            return Response({"message": "Dashboard published successfully."}, status=status.HTTP_200_OK)
        except Dashboard.DoesNotExist:
            raise PermissionDenied("Dashboard not found or you do not have permission to publish it.")


class EmbedStaticDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanEmbedDashboardPermission]
    
    def get(self, request, *args, **kwargs):       
        try:
            dashboard_id = kwargs.get('dashboard_id')
            dashboard = Dashboard.objects.get(id=dashboard_id)
            self.check_object_permissions(request, dashboard)
            return Response({
                'embed_url': get_embed_metabase_url(dashboard_id, request)}, status=status.HTTP_200_OK)
        except Dashboard.DoesNotExist:
            raise PermissionDenied("Dashboard not found or you do not have permission to view it.")


class EmebedSDKDashboardView(APIView):
    permission_classes = [IsAuthenticated, CanViewDashboardPermission]
    
    def get(self, request, *args, **kwargs):
        try:
            dashboard_id = kwargs.get('dashboard_id')
            dashboard = Dashboard.objects.get(id=dashboard_id)
            
            if not request.user.has_perm('dashboards.view_dashboard'):
                raise PermissionDenied("You do not have permission to view this dashboard.")
            
            embed_url = get_embed_metabase_url(dashboard_id, request)
            return render(request, 'embed_sdk_dashboard.html', {'embed_url': embed_url})
        except Dashboard.DoesNotExist:
            raise PermissionDenied("Dashboard not found or you do not have permission to view it.")