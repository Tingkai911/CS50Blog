from django.urls import path
# to send the request to views.py and return the correct response
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView, 
    likeView,
    dislikeView, 
    commentView,
    commentDelete
)

urlpatterns = [
    # name='blog-home' to do reverse lookup on this route if necessary
    # path('', views.home, name='blog-home'),
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('like/<int:pk>', likeView, name="like-post"),
    path('dislike/<int:pk>', dislikeView, name="dislike-post"),
    path('comment/<int:pk>/<str:username>', commentView, name="comment-post"),
    path('comment/delete/<int:pk>/<int:id>', commentDelete, name='comment-delete'),
]