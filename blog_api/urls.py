from django.urls import path
from .views import PostList, PostDetail, UserPostList


urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('', PostList.as_view(), name='post_list'),
    path('user/<int:id>/', UserPostList.as_view()),
]