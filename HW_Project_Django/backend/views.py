from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404

from backend.models import User, Post, Comment
from backend.serializers import *


class UserListCreateView(APIView):
    def get(self, request):
        users = User.objects.annotate(posts_count=Count('post')).order_by('id')
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserDetailView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserCreateSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserCreateSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        user.delete()
        return Response(
            status=status.HTTP_200_OK
        )


class UserPostsView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        posts = Post.objects.filter(author=user).annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True),
        )
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)


class UserStatsView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        stats = User.objects.filter(pk=user.pk).aggregate(
            total_posts=Count('post', distinct=True),
            total_comments=Count('post__comment', distinct=True),
        )
        stats['user_id'] = user.id
        stats['user_name'] = user.user_name
        stats['total_likes_given'] = (user.liked_posts.count() + user.liked_comments.count())
        return Response(stats)


class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.select_related('author').annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True),
        )
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post.objects.select_related('author'), pk=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostCreateSerializer(post, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = PostCreateSerializer(post, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        post.delete()
        return Response(status=status.HTTP_200_OK)


class PostLikeView(APIView):
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id не валиден'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if post.likes.filter(pk=user.pk).exists():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        return Response({
            'post_id': post.id,
            'user_id': user.id,
            'liked': liked,
            'total_likes': post.likes.count(),
        })


class PostCommentsView(APIView):
    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Пост не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        comments = Comment.objects.filter(post=post).select_related('author').annotate(likes_count=Count('likes'))
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)


class CommentListCreateView(APIView):
    def get(self, request):
        comments = Comment.objects.select_related('author', 'post').annotate(likes_count=Count('likes'))
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentDetailView(APIView):
    def get(self, request, pk):
        comment = get_object_or_404(
            Comment.objects.select_related('author', 'post'), pk=pk
        )
        serializer = CommentDetailSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Комментарий не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentCreateSerializer(comment, data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )            
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Комментарий не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CommentCreateSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Комментарий не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        comment.delete()
        return Response(status=status.HTTP_200_OK)


class CommentLikeView(APIView):
    def post(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Комментарий не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id не валиден'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        if comment.likes.filter(pk=user.pk).exists():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True
        return Response({
            'comment_id': comment.id,
            'user_id': user.id,
            'liked': liked,
            'total_likes': comment.likes.count(),
        })
