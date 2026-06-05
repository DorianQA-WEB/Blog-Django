"""
URL-конфигурация приложения blog.

Определяет маршруты для основных функций блога:
- Список постов (с возможностью фильтрации по тегу)
- Детальный просмотр поста
- Поделиться постом (email)
- Добавление комментария
- Поиск постов
Пространство имён: 'blog'
Примеры URL:
  /blog/                    → список постов
  /blog/2026/4/10/my-post/  → детальный просмотр
  /blog/tag/python/         → посты с тегом 'python'
  /blog/search/             → поиск

Маршруты:
---------
1. `/` → post_list
   - Отображает список всех опубликованных постов
   - Поддерживает пагинацию и фильтрацию по тегу
2. `/year/month/day/slug/` → post_detail
   - Детальный просмотр одного поста
   - Параметры: год, месяц, день, slug (человекопонятный URL)
   - Пример: /2026/4/10/my-first-post/

3. `/post_id/share/` → post_share
   - Страница отправки поста по электронной почте
   - Использует EmailPostForm

4. `/post_id/comment/` → post_comment
   - Обработка и отображение комментариев к посту
   - Поддерживает POST-запросы для добавления комментариев

5. `/tag/tag_slug/` → post_list
   - Фильтрация постов по тегу
   - Пример: /tag/python/ → все посты с тегом "python"

6. `/search/` → post_search
   - Поиск постов по тексту заголовка и содержания
   - Использует SearchForm и Post.objects.filter(...)

Примечания:
-----------
- Используются функциональные представления (FBV), а не классовые (CBV)
- Для тегов и поиска используются кастомные методы в модели/менеджере
- URL-параметры: `int` для дат, `slug` для читаемых имен
- Маршруты могут быть расширены в будущем (API, RSS и т.д.)
Ошибки и предупреждения:
-----------------------
- Комментированные строки `views.PostListView` указывают, что ранее
  использовались классовые представления, но сейчас включены FBV
- В `settings.py` должен быть настроен `app_name = 'blog'` для
  корректной работы `reverse()` и `{% url 'blog:name' %}`
"""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # представления поста
    # path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list')
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('search/', views.post_search, name='post_search'),
]