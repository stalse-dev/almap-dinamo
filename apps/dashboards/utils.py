import os
import jwt
from apps.dashboards.models import Dashboard
from rest_framework.exceptions import PermissionDenied

METABASE_EMBEDDING_BASE_URL = os.environ.get("METABASE_EMBEDDING_BASE_URL", "http://localhost:5500")
METABASE_SECRET_KEY = os.environ.get("METABASE_SECRET_KEY", "your-metabase-secret-key")

def get_embed_metabase_url(dashboard_id, request, **kwargs):
    dashboard = Dashboard.objects.get(id=dashboard_id)
    payload = {
        "resource": {
            "dashboard": dashboard.embed_url
        },
        "params": {
            "id": request.user.firebase_uid,
        }
    }
    token = get_token_metabase(payload)
    return f"{METABASE_EMBEDDING_BASE_URL}/embed/dashboard/{token}#bordered=true"
    
    
    
def get_token_metabase(payload):
    """
    Generate a JWT token for embedding Metabase dashboards.
    """
    secret_key = METABASE_SECRET_KEY
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

