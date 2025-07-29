from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from apps.core.auth import FirebaseAuthentication

User = get_user_model()


class FirebaseAuthenticationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.auth = FirebaseAuthentication()
        self.id_token = "test_id_token"
        self.firebase_uid = "firebase_uid_123"
        self.email = "test@example.com"
        self.name = "Test User"
        self.picture = "http://example.com/avatar.png"
        self.decoded_token = {
            "uid": self.firebase_uid,
            "email": self.email,
            "name": self.name,
            "picture": self.picture,
        }

    @patch("apps.core.auth.cache")
    @patch("apps.core.auth.auth.verify_id_token")
    def test_authenticate_success(self, mock_verify_id_token, mock_cache):
        mock_cache.get.return_value = None
        mock_verify_id_token.return_value = self.decoded_token
        mock_cache.set = MagicMock()

        request = self.factory.get("/", HTTP_AUTHORIZATION=f"Bearer {self.id_token}")
        user, _ = self.auth.authenticate(request)

        self.assertEqual(user.firebase_uid, self.firebase_uid)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.avatar_url, self.picture)
        mock_cache.set.assert_called_once()
        mock_verify_id_token.assert_called_once_with(self.id_token)

    @patch("apps.core.auth.cache")
    def test_authenticate_with_cached_token(self, mock_cache):
        mock_cache.get.return_value = self.decoded_token
        mock_cache.set = MagicMock()

        request = self.factory.get("/", HTTP_AUTHORIZATION=f"Bearer {self.id_token}")
        with patch("apps.core.auth.auth.verify_id_token") as mock_verify_id_token:
            user, _ = self.auth.authenticate(request)
            self.assertEqual(user.firebase_uid, self.firebase_uid)
            mock_verify_id_token.assert_not_called()

    def test_authenticate_no_header(self):
        request = self.factory.get("/")
        result = self.auth.authenticate(request)
        self.assertIsNone(result)

    def test_authenticate_invalid_header(self):
        request = self.factory.get("/", HTTP_AUTHORIZATION="InvalidToken")
        result = self.auth.authenticate(request)
        self.assertIsNone(result)

    @patch("apps.core.auth.cache")
    @patch("apps.core.auth.auth.verify_id_token")
    def test_authenticate_firebase_error(self, mock_verify_id_token, mock_cache):
        mock_cache.get.return_value = None
        mock_verify_id_token.side_effect = Exception("Invalid token")
        request = self.factory.get("/", HTTP_AUTHORIZATION=f"Bearer {self.id_token}")
        with self.assertRaises(AuthenticationFailed):
            self.auth.authenticate(request)
