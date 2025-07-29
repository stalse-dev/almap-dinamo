from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view as drf_get_schema_view 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.dashboards.urls')),
]
# Documentação nativa do DRF
API_TITLE = "Permadata API"
API_DESCRIPTION = "Documentação básica da API (DRF nativo)"

urlpatterns += [
    path("", include_docs_urls(
        title=API_TITLE,
        description=API_DESCRIPTION,
        permission_classes=[AllowAny],
    )),
    path("schema-basic/", drf_get_schema_view(  # <- Usando o nome correto aqui
        title=API_TITLE,
        description=API_DESCRIPTION,
        version="1.0.0",
        permission_classes=[AllowAny]
    ), name="basic-schema"),
]
