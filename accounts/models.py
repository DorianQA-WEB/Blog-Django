from django.db import models
from django.contrib.auth.models import User
from PIL import Image


"""Profile model 

Описание:
Модель Profile расширяет стандартную модель User одним-ко-одному связью и хранит аватар и биографию.

Поля:
user (OneToOneField): связь с django.contrib.auth.models.User, on_delete=models.CASCADE.
avatar (ImageField): изображение профиля, upload_to='profile_images', по умолчанию 'default.jpg'.
bio (TextField): текст биографии пользователя.

Поведение:
- str возвращает username связанного пользователя.
- save() сохраняет модель, затем открывает загруженный файл avatar и при большем размере, чем 100x100,
уменьшает изображение до минимума 100x100 посредством thumbnail и перезаписывает файл.
"""
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

