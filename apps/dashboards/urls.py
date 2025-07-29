from rest_framework.routers import DefaultRouter
from .views import DashboardViewSet

router = DefaultRouter()
router.register(r'dashboards', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls