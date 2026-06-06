"""
Модуль представлений (views) для API приложения blog_api.

Определяет RESTful API-эндпоинты для работы с постами:
- Список и создание постов (PostList)
- Детальный просмотр, редактирование и удаление (PostDetail)
- Список постов текущего пользователя (UserPostList)

Особенности:
-------------
- Используются классовые представления DRF (generics)
- Поддержка DRF-фильтрации через `DjangoFilterBackend`
- Кастомное разрешение `IsAuthorOrReadOnly`:
  - GET/HEAD/OPTIONS: доступ всем
  - POST: только авторизованным
  - PUT/PATCH/DELETE: только автор поста
- Фильтрация по `author` (например: `/api/?author=1`)
- `UserPostList` возвращает только посты текущего пользователя

Структура эндпоинтов:
---------------------
GET  /api/              → List (PostList)
POST /api/              → Create (PostList)
GET  /api/{id}/         → Retrieve (PostDetail)
PUT  /api/{id}/         → Update (PostDetail)
PATCH /api/{id}/        → Partial Update (PostDetail)
DELETE /api/{id}/       → Destroy (PostDetail)
GET  /api/my-posts/     → List по текущего пользователя (UserPostList)

Ошибки и предупреждения:
------------------------
- `permissions_classes = [...]` в `PostDetail` закомментировано —
  устаревший код с ошибкой в имени атрибута
- `permission_classes = (IsAuthorOrReadOnly,)` — кортеж, но можно и список
- В `UserPostList` не установлено `permission_classes`, что может быть небезопасно
"""
from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    API-эндпоинт для получения списка постов и создания новых.

    Разрешения:
        - GET: все (включая анонимных)
        - POST: только авторизованные (IsAuthorOrReadOnly)
    Фильтрация:
        - По полю `author`: /api/?author=1
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author']


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API-эндпоинт для детального просмотра, редактирования и удаления поста.

    Разрешения:
        - GET: все
        - PUT/PATCH/DELETE: только автор поста
    """
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permissions_classes = [permissions.IsAdminUser,]


class UserPostList(generics.ListAPIView):
    """
    API-эндпоинт для получения постов текущего пользователя.

    Разрешения:
        - GET: только авторизованные (должно быть: permission_classes = [IsAuthenticated])
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        Возвращает посты авторизованного пользователя.

        Returns:
            QuerySet[Post]: Только посты, созданные текущим пользователем
        """
        user = self.request.user
        return Post.objects.filter(author=user)


