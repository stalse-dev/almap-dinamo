from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()

class FirebaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Obtém o header de autorização
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header.startswith("Bearer "):
            return None  # Nenhum token informado, ignora essa autenticação

        # Extrai o token JWT
        id_token = auth_header.split("Bearer ")[1]
        cache_key = f"firebase_token:{id_token}"

        # Tenta obter o token decodificado do cache
        decoded_token = cache.get(cache_key)

        try:
            # Se não estiver no cache, verifica com o Firebase e salva no cache
            if not decoded_token:
                decoded_token = auth.verify_id_token(id_token)
                cache.set(cache_key, decoded_token, timeout=300)  # Cache por 5 minutos

            # Extrai informações do token
            firebase_uid = decoded_token["uid"]
            email = decoded_token.get("email")
            name = decoded_token.get("name", "")
            picture = decoded_token.get("picture", "")

            # Divide o nome em primeiro e último nome (se possível)
            first_name = name.split()[0] if name else ""
            last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else ""

            # Busca ou cria o usuário localmente com base no UID do Firebase
            user, created = User.objects.get_or_create(
                firebase_uid=firebase_uid,
                defaults={
                    "username": email or firebase_uid,
                    "email": email or "",
                    "first_name": first_name,
                    "last_name": last_name,
                    "picture_url": picture,
                },
            )

            return (user, None)

        except Exception as e:
            raise AuthenticationFailed(f"Token inválido: {e}")
