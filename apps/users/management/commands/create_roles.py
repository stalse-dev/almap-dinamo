from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):
    help = "Cria os cargos (roles) padrão no sistema"

    def handle(self, *args, **kwargs):
        roles_data = [
            ("Master Admin", "Controle total da plataforma"),
            ("Gestor de Área", "Gerencia dashboards e membros da área"),
            ("Analista (BI)", "Cria e propõe dashboards"),
            ("Viewer", "Visualiza dashboards da sua área"),
            ("Viewer Global", "Visualiza todos os dashboards da plataforma"),
        ]

        created = 0
        for name, desc in roles_data:
            role, was_created = Role.objects.get_or_create(name=name, defaults={"description": desc})
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"{created} cargo(s) criado(s) com sucesso."))
