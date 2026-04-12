from django.urls import path
from .views import Postlist, PostDetail


urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', Postlist.as_view(), name='post_list'),
]