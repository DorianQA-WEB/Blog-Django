from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



class PublishedManager(models.Manager):
    """
    Кастомный менеджер модели Post.

    Фильтрует объекты, возвращая только опубликованные посты.
    Используется как `Post.published.all()` для получения
    только тех постов, у которых status='PB' (Published).
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    """
    Модель блог-поста.

    Представляет собой статью в блоге с заголовком, содержанием,
    автором, датой публикации и статусом. Поддерживает теги
    через django-taggit.

    Атрибуты:
        title (str): Заголовок поста (до 250 символов)
        slug (str): URL-дружественное имя, уникальное на дату публикации
        author (User): Связь с пользователем Django (ForeignKey)
        body (str): Текст поста
        publish (datetime): Дата и время публикации
        created (datetime): Дата и время создания (авто)
        updated (datetime): Дата и время последнего изменения (авто)
        status (str): Статус поста — черновик или опубликован
        tags (TaggableManager): Управление тегами
            Менеджеры:
        objects (Manager): Стандартный менеджер
        published (PublishedManager): Только опубликованные посты

    Индексы:
        - Индекс по полю `publish` для ускорения сортировки

    Сортировка: по убыванию даты публикации
    """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now) # поле даты публикации
    created = models.DateTimeField(auto_now_add=True) # поле даты создания
    updated = models.DateTimeField(auto_now=True) # поле даты изменения
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()# менеджер, применяемый по умолчанию
    published = PublishedManager()# менеджер для статей, опубликованных на сайте
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def get_absolute_url(self):
        """
        Возвращает канонический URL для поста.

        Используется в шаблонах и при редиректах после создания/редактирования.
        Пример: /2026/4/10/my-post/

        Returns:
            str: Абсолютный URL поста
        """
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Модель комментария к посту.

    Позволяет читателям оставлять комментарии под постами.
    Поддерживает модерацию через поле `active`.

    Атрибуты:
        post (Post): Связь с постом (ForeignKey)
        name (str): Имя комментатора (до 80 символов)
        email (str): Email комментатора
        body (str): Текст комментария
        created (datetime): Дата создания (авто)
        updated (datetime): Дата обновления (авто)
        active (bool): Статус активности (по умолчанию True)
    Мета:
        ordering: по возрастанию даты создания
        indexes: индекс по `created` для производительности

    Методы:
        __str__: Возвращает описание комментария
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Комментарий от {self.name} к посту {self.post}'

