"""
Модуль представлений (views) для приложения blog.

Определяет обработчики HTTP-запросов для:
- Списка постов (с пагинацией и фильтрацией по тегу)
- Детального просмотра одного поста
- Отправки поста по электронной почте
- Добавления комментариев
- Поиска постов по сходству текста

Ключевые особенности:
---------------------
- Используются функциональные представления (FBV), а не классовые (CBV)
- Поддержка пагинации через `django.core.paginator.Paginator`
- Встроенный поиск PostgreSQL через `TrigramSimilarity`
- Валидация форм и обработка ошибок
- Отправка email через `django.core.mail.send_mail`

Ошибки и исправления:
---------------------
1. В `post_share` — синтаксическая ошибка f-строки:
   - Было: `f'{cd['name']} recommends...'` → невалидно, кавычки внутри кавычек
   - Стало: `f"{cd['name']} recommends..."` → правильно

2. В `post_search` — добавлено:
   - Проверка `if form.is_valid():` перед использованием cleaned_data
   - Гарантированная инициализация `form`, `query`, `results`

Документация:
-------------
"""
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST

from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity

# class PostListView(ListView):
#     """
#     Альтернативное представление списка постов
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """
    Отображает список опубликованных постов с пагинацией.

    Параметры:
        request (HttpRequest): Объект запроса
        tag_slug (str, optional): Slug тега для фильтрации постов

    Возвращает:
        HttpResponse: Страница со списком постов

    Детали:
        - Показывает по 3 поста на страницу
        - Поддерживает фильтрацию по тегу
        - Обрабатывает ошибки пагинации (нецелое число, вне диапазона)
    """
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то
        # выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, slug):
    """
    Отображает детальную информацию об одном посте.

    Параметры:
        request (HttpRequest)
        year (int): Год публикации
        month (int): Месяц публикации
        day (int): День публикации
        slug (str): Человекопонятное имя поста

    Возвращает:
        HttpResponse: Страница с деталями поста, комментариями и похожими постами

    Детали:
        - Загружает 4 похожих поста по общим тегам
        - Подготавливает форму для добавления комментария
        - Фильтрует только активные комментарии
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментирования пользователями
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})


def post_share(request, post_id):
    """
    Отправляет пост по электронной почте.

    Параметры:
        request (HttpRequest)
        post_id (int): Идентификатор поста

    Возвращает:
        HttpResponse: Страница формы или подтверждение отправки

    Детали:
        - Поддерживает методы GET и POST
        - Валидация EmailPostForm
        - Отправка email через `send_mail`
        - Генерация абсолютного URL поста
    """
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
    # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f'{cd['name']} recommends you read {post.title}'
            message = f'Read {post.title} at {post_url}\n\n {cd['name']}\'s ({cd['email']}) comments: {cd['comments']}'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['to']])
            sent = True
            # ... отправить электронное письмо
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    """
    Обрабатывает отправку комментария к посту.

    Параметры:
        request (HttpRequest)
        post_id (int): Идентификатор поста

    Возвращает:
        HttpResponse: Страница с постом и результатом комментирования

    Детали:
        - Только POST-запросы (декоратор `require_POST`)
        - Создаёт комментарий, связывает с постом
        - Не сохраняет в БД без `commit=False`
    """
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    return render(request, 'blog/post/comment.html',
                  {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    """
    Выполняет поиск постов по сходству текста.

    Параметры:
        request (HttpRequest)

    Возвращает:
        HttpResponse: Страница результатов поиска

    Детали:
        - Использует PostgreSQL-функцию TrigramSimilarity
        - Порог сходства: > 0.1
        - Результаты сортируются по убыванию сходства
        - Безопасная инициализация переменных
    """
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


