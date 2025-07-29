from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.core.cache import cache
import firebase_admin
from firebase_admin import auth

User = get_user_model()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # DRF vai tentar os próximos métodos

        id_token = auth_header.split("Bearer ")[1]
        cache_key = f"firebase_token:{id_token}"
        decoded_token = cache.get(cache_key)

        try:
            if not decoded_token:
                decoded_token = auth.verify_id_token(id_token)
                cache.set(cache_key, decoded_token, timeout=300)

            firebase_uid = decoded_token["uid"]
            email = decoded_token.get("email")
            name = decoded_token.get("name", "")
            picture = decoded_token.get("picture", "")

            user, _ = User.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    "username": email or firebase_uid,
                    "email": email or "",
                    "first_name": name.split()[0] if name else "",
                    "last_name": " ".join(name.split()[1:]) if name else "",
                    "avatar_url": picture,
                },
            )


            return (user, None)

        except Exception as e:
            raise AuthenticationFailed(f"Firebase authentication failed: {e}")
