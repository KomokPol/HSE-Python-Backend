from rest_framework import serializers
from backend.models import User, Post, Comment


class UserListSerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'user_name', 'email', 'posts_count']


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.user_name', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_name', 'likes_count', 'comments_count', 'created']


class CommentListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.user_name', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'post', 'body', 'likes_count', 'created']


class UserDetailSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    liked_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'user_name', 'age', 'email', 'posts_count', 'liked_posts_count']

    def get_posts_count(self, obj):
        return obj.post_set.count()

    def get_liked_posts_count(self, obj):
        return obj.liked_posts.count()


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.user_name', read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    comments = CommentListSerializer(source='comment_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'author_name', 'body',
                  'likes_count', 'comments_count', 'comments',
                  'created', 'updated']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()


class CommentDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.user_name', read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'post', 'body',
                  'likes_count', 'created', 'updated']

    def get_likes_count(self, obj):
        return obj.likes.count()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'user_name', 'age', 'email']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'author', 'body']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'body']
