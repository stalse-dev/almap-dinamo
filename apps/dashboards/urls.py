from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.dashboards.views import *

router = DefaultRouter()
router.register(r"dashboards", DashboardViewSet, basename="dashboard")
router.register(r"group_dashboard", GroupDashboardViewSet, basename="dashboard-group")

urlpatterns = router.urls + [
    path(
        "dashboards/<int:dashboard_id>/embed/static/",
        EmbedStaticDashboardView.as_view(),
        name="embed-dashboard",
    ),
    path(
        "dashboards/<int:dashboard_id>/approve",
        ApproveDashboardView.as_view(),
        name="approve-dashboard",
    ),
    path(
        "dashboards/details",
        AccessibleDashboardsView.as_view(),
        name="accessible-dashboards",
    ),
]
