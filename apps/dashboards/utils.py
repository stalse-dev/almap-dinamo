import os
import jwt
from apps.dashboards.models import Dashboard
from rest_framework.exceptions import PermissionDenied


def get_embedded_url(dashboard_id, request, **kwargs):
    embedded_type = os.environ.get("EMBEDDED_TYPE")
    match embedded_type:
        case "METABASE":
            METABASE_EMBEDDING_BASE_URL = os.environ.get(
                "METABASE_EMBEDDING_BASE_URL", "http://localhost:5500"
            )
            METABASE_SECRET_KEY = os.environ.get(
                "METABASE_SECRET_KEY", "your-metabase-secret-key"
            )
            return METABASE_EMBEDDING_BASE_URL + get_embed_metabase_url(
                dashboard_id, request, METABASE_SECRET_KEY, **kwargs
            )

        case "POWER_BI":
            pass

        case _:
            raise PermissionDenied(
                "Invalid EMBEDDED_TYPE. Supported types are: METABASE, POWER_BI."
            )


def get_embed_metabase_url(dashboard_id, request, secret_key, **kwargs):
    dashboard = Dashboard.objects.get(id=dashboard_id)
    payload = {
        "resource": {"dashboard": dashboard.embed_url},
        "params": {
            "id": request.user.firebase_uid,
        },
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return f"/embed/dashboard/{token}#bordered=true"
