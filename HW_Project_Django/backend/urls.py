from django.urls import path
from backend.views import *

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='UserListCreate'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='UserDetail'),
    path('users/<int:pk>/posts/', UserPostsView.as_view(), name='UserPosts'),
    path('users/<int:pk>/stats/', UserStatsView.as_view(), name='UserStats'),

    path('posts/', PostListCreateView.as_view(), name='PostListCreate'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='PostDetail'),
    path('posts/<int:pk>/like/', PostLikeView.as_view(), name='PostLike'),
    path('posts/<int:pk>/comments/', PostCommentsView.as_view(), name='PostComments'),

    path('comments/', CommentListCreateView.as_view(), name='CommentListCreate'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='CommentDetail'),
    path('comments/<int:pk>/like/', CommentLikeView.as_view(), name='CommentLike'),
]
