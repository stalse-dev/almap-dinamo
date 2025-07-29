# apps/core/permissions.py

from rest_framework.permissions import IsAuthenticated, AllowAny

class AllowAnyForDocsOrIsAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        if request.path.startswith('/docs/') or request.path == '/schema-basic/':
            return True  # Libera acesso à doc
        return super().has_permission(request, view)
