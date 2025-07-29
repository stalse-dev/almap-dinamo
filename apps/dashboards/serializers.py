from rest_framework import serializers
from apps.dashboards.models import Dashboard, GroupDashboard


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = "__all__"


class DashboardCreateSerializer(serializers.ModelSerializer):
    group_dashboard_id = serializers.PrimaryKeyRelatedField(
        queryset=GroupDashboard.objects.all(),
        write_only=True,
        required=True,
        help_text="ID do GroupDashboard ao qual o dashboard será vinculado.",
    )

    class Meta:
        model = Dashboard
        fields = ["id", "title", "embed_url", "description", "group_dashboard_id"]


class DashboardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = ["id", "title", "status"]


class GroupDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDashboard
        fields = ["id", "name", "dashboards"]


class GroupDashboardRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDashboard
        fields = ["id", "name", "description", "tags", "dashboards", "users"]


class GroupDashboardCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDashboard
        fields = ["id", "name", "description", "tags", "dashboards"]


class GroupDashboardUpdateSerializer(serializers.ModelSerializer):
    # Exemplo: deixa 'name' obrigatório e 'description' opcional
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = GroupDashboard
        fields = ["id", "name", "description", "tags", "dashboards", "users"]
