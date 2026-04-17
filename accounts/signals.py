from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Создаёт связанный Profile и токен аутентификации при создании нового пользователя.

    Аргументы:
        sender: Класс модели, от которого пришёл сигнал (обычно django.contrib.auth.models.User).
        instance: Экземпляр модели User, для которого был вызван сигнал.
        created (bool): True, если экземпляр был создан (не обновлён).
        **kwargs: Дополнительные параметры сигнала.

    Побочные эффекты:
        - Создаётся объект Profile, связанный с instance.
        - Создаётся объект Token для instance (используется DRF TokenAuthentication).
    """
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)

