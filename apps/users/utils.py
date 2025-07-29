from django.contrib.auth import get_user_model

User = get_user_model()

def get_or_create_firebase_user(firebase_data):
    uid = firebase_data.get("uid")
    email = firebase_data.get("email")
    name = firebase_data.get("name", "")
    picture = firebase_data.get("picture", "")

    user, created = User.objects.get_or_create(
        firebase_uid=uid,
        defaults={
            "username": email,
            "email": email,
            "first_name": name.split(" ")[0],
            "last_name": " ".join(name.split(" ")[1:]),
            "avatar_url": picture,
        }
    )

    # opcional: atualiza campos como imagem ou nome se mudarem
    if not created:
        updated = False
        if user.email != email:
            user.email = email
            updated = True
        if hasattr(user, "avatar_url") and user.avatar_url != picture:
            user.avatar_url = picture
            updated = True
        if updated:
            user.save()

    return user
