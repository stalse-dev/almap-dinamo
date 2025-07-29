from django.test import TestCase

# Create your tests here.

from unittest.mock import patch, MagicMock
from django.contrib.auth.models import AnonymousUser
from apps.dashboards.utils import get_embed_metabase_url, get_token_metabase
from apps.dashboards.models import Dashboard
import jwt


class MetabaseEmbeddingTests(TestCase):
    def setUp(self):
        self.dashboard = Dashboard.objects.create(id=1, embed_url="test-dashboard-url")
        self.request = MagicMock()
        self.request.user = MagicMock()
        self.request.user.firebase_uid = "test-firebase-uid"
        self.metabase_secret_key = "test-secret-key"
        self.metabase_base_url = "http://metabase.example.com"

    @patch(
        "apps.dashboards.utils.METABASE_EMBEDDING_BASE_URL",
        "http://metabase.example.com",
    )
    @patch("apps.dashboards.utils.get_token_metabase")
    def test_get_embed_metabase_url_success(self, mock_get_token_metabase):
        mock_get_token_metabase.return_value = "test-token"
        expected_url = (
            "http://metabase.example.com/embed/dashboard/test-token#bordered=true"
        )

        result = get_embed_metabase_url(self.dashboard.id, self.request)

        self.assertEqual(result, expected_url)
        mock_get_token_metabase.assert_called_once_with(
            {
                "resource": {"dashboard": self.dashboard.embed_url},
                "params": {"id": "test-firebase-uid"},
            }
        )

    @patch("apps.dashboards.utils.jwt.encode")
    @patch("apps.dashboards.utils.METABASE_SECRET_KEY", "test-secret-key")
    def test_get_token_metabase_success(self, mock_jwt_encode):
        payload = {
            "resource": {"dashboard": "test-dashboard-url"},
            "params": {"id": "test-firebase-uid"},
        }
        mock_jwt_encode.return_value = "encoded-jwt-token"

        result = get_token_metabase(payload)

        self.assertEqual(result, "encoded-jwt-token")
        mock_jwt_encode.assert_called_once_with(
            payload, "test-secret-key", algorithm="HS256"
        )

    @patch(
        "apps.dashboards.utils.METABASE_EMBEDDING_BASE_URL",
        "http://metabase.example.com",
    )
    def test_get_embed_metabase_url_invalid_dashboard(self):
        with self.assertRaises(Dashboard.DoesNotExist):
            get_embed_metabase_url(999, self.request)

    def test_get_embed_metabase_url_anonymous_user(self):
        self.request.user = AnonymousUser()

        with self.assertRaises(AttributeError):
            get_embed_metabase_url(self.dashboard.id, self.request)


class PermissionTests(TestCase):
    def setUp(self):
        self.user = MagicMock()
        self.user.is_authenticated = True
        self.user.has_perm = MagicMock(return_value=True)
        self.user.group = MagicMock(name="Teste")
        self.request = MagicMock()
        self.request.user = self.user
        self.obj = MagicMock()

    def test_user_has_permission(self):
        from apps.dashboards.permissions import CanApproveDashboardPermission

        self.user.has_perm = MagicMock(return_value=True)
        permission = CanApproveDashboardPermission()
        self.assertTrue(permission.has_object_permission(self.request, None, self.obj))

    def test_user_has_not_permission(self):
        from apps.dashboards.permissions import CanApproveDashboardPermission

        self.user.has_perm = MagicMock(return_value=False)
        permission = CanApproveDashboardPermission()
        self.assertFalse(permission.has_object_permission(self.request, None, self.obj))
