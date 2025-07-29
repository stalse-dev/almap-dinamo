from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group


class Command(BaseCommand):
    help = "Cria os cargos (roles) padrão no sistema"

    def handle(self, *args, **kwargs):
        # Cria os cargos (roles) padrão no sistema
        roles_data = [
            ("Master Admin", "Controle total da plataforma"),
            ("Gestor de Área", "Gerencia dashboards e membros da área"),
            ("Analista (BI)", "Cria e propõe dashboards"),
            ("Viewer", "Visualiza dashboards da sua área"),
            ("Viewer Global", "Visualiza todos os dashboards da plataforma"),
        ]

        view_dashboard_permissions = Permission.objects.get(codename="view_dashboard")
        view_global_dashboard_permissions = Permission.objects.get(codename="can_view_global_dashboard")
        edit_dashboard_permissions = Permission.objects.get(codename="change_dashboard")
        create_dashboard_permissions = Permission.objects.get(codename="add_dashboard")
        publish_dashboard_permissions = Permission.objects.get(codename="can_publish_dashboard")
        approve_dashboard_permissions = Permission.objects.get(codename="can_approve_dashboard")
        delete_dashboard_permissions = Permission.objects.get(codename="delete_dashboard")
        
        create_workspace_permissions = Permission.objects.get(codename="add_workspace")
        view_workspace_permissions = Permission.objects.get(codename="view_workspace")
        edit_workspace_permissions = Permission.objects.get(codename="change_workspace")
        delete_workspace_permissions = Permission.objects.get(codename="delete_workspace")
        
        
        viewer_group, _ = Group.objects.get_or_create(name="Viewer")
        viewer_group.permissions.add(view_dashboard_permissions)
        
        viewer_global_group, _ = Group.objects.get_or_create(name="Viewer Global")
        viewer_global_group.permissions.add(view_global_dashboard_permissions)
        
        editor_group, _ = Group.objects.get_or_create(name="Analista (BI)")
        editor_group.permissions.add(
            view_dashboard_permissions,
            edit_dashboard_permissions,
            create_dashboard_permissions,
            delete_dashboard_permissions,
            publish_dashboard_permissions,
        )
        
        manager_group, _ = Group.objects.get_or_create(name="Gestor de Área") 
        manager_group.permissions.add(
            view_dashboard_permissions,
            edit_dashboard_permissions,
            create_dashboard_permissions,
            delete_dashboard_permissions,
            publish_dashboard_permissions,
            approve_dashboard_permissions,
            create_workspace_permissions,
            view_workspace_permissions,
            edit_workspace_permissions,
            delete_workspace_permissions
        )

        self.stdout.write(self.style.SUCCESS("Todos os cargos foram criados ou já existiam."))