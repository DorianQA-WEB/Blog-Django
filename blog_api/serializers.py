from rest_framework import serializers
from blog.models import Post


"""PostSerializer

ModelSerializer для модели Post.

Attributes (поля):
id (int): Уникальный идентификатор записи. Read-only.
author (User): Скрытое поле, автоматически устанавливается в текущего аутентифицированного пользователя
через serializers.HiddenField(default=serializers.CurrentUserDefault()). Клиент не передаёт это поле.
title (str): Заголовок поста.
body (str): Содержимое поста.
created (datetime): Дата и время создания записи. Read-only.
status (str): Статус поста (использует choices, заданные в модели Post).
slug (str): Человеко-читаемый идентификатор для URL. Обычно read-only (генерируется в модели).

Behavior (поведение):
- При создании экземпляра author автоматически заполняется из request.user.
- Валидация полей выполняется на основе определений модели; для дополнительных правил можно
добавить методы validate_() или общий validate().
- Если slug должен генерироваться автоматически — реализация должна быть в модели (save() или сигнал)
либо в переопределённом create() сериализатора.

Usage (рекомендации):
- Рекомендуется явно указать read_only_fields в Meta:
read_only_fields = ('id', 'created', 'slug', 'author')
- Для возврата данных автора (имя, email) можно добавить read-only поле (SerializerMethodField или вложенный
сериализатор), сохранив HiddenField для установки автора при создании.
- В ViewSet/GenericAPIView разрешить создание/редактирование только для аутентифицированных пользователей.

Example Meta:
class Meta:
model = Post
fields = ('id', 'author', 'title', 'body', 'created', 'status', 'slug')
read_only_fields = ('id', 'created', 'slug', 'author')
"""
class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        fields = (
            'id',
            'author',
            'title',
            'body',
            'created',
            'status',
            'slug',
        )
        model = Post