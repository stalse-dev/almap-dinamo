from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def add_user_to_default_group(sender, instance, created, **kwargs):
    if created:  # Verifica se o usuário foi criado
        default_group, _ = Group.objects.get_or_create(name="Viewer")
        instance.groups.add(default_group)
