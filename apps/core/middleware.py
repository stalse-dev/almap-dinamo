import firebase_admin
from firebase_admin import auth
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class FirebaseAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header or not auth_header.startswith("Bearer "):
            request.user = AnonymousUser()
            return

        id_token = auth_header.split("Bearer ")[1]

        # Cache key por token (ajuda muito com performance se Redis ativo)
        cache_key = f"firebase_token:{id_token}"
        decoded_token = cache.get(cache_key)

        try:
            if not decoded_token:
                decoded_token = auth.verify_id_token(id_token)
                cache.set(cache_key, decoded_token, timeout=300)  # 5 min

            firebase_uid = decoded_token["uid"]
            email = decoded_token.get("email")
            name = decoded_token.get("name", "")
            picture = decoded_token.get("picture", "")

            user, created = User.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    "username": email or firebase_uid,
                    "email": email or "",
                    "first_name": name.split()[0] if name else "",
                    "last_name": " ".join(name.split()[1:]) if name else "",
                    "picture_url": picture,
                },
            )

            request.user = user

        except Exception as e:
            logger.warning(f"[FirebaseAuthMiddleware] Erro na autenticação: {e}")
            request.user = AnonymousUser()

