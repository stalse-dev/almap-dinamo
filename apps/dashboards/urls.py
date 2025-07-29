from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.dashboards.views import *

router = DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'workspace', WorkSpaceViewSet, basename='dashboard-workspace')

urlpatterns = router.urls + [
    path('dashboards/embed/static/<int:dashboard_id>/', EmbedStaticDashboardView.as_view(), name='embed-dashboard'),
    path('dashboards/approve/<int:dashboard_id>/', ApproveDashboardView.as_view(), name='approve-dashboard'),
    path('dashboards/publish/<int:dashboard_id>/', PublishDashboardView.as_view(), name='publish-dashboard'),
]