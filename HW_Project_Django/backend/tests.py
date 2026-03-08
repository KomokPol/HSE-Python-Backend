from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token
from backend.models import User, Post, Comment


class AuthTests(APITestCase):
    def test_register(self):
        response = self.client.post('/api/register/', {
            'username': 'Polina', 'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login(self):
        AuthUser.objects.create_user(username='Polina', password='password123')
        response = self.client.post('/api/login/', {
            'username': 'Polina', 'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        AuthUser.objects.create_user(username='Polina', password='password123')
        response = self.client.post('/api/login/', {
            'username': 'Polina', 'password': 'alarm'
        })
        self.assertEqual(response.status_code, 401)


class UserTests(APITestCase):
    def setUp(self):
        self.auth_user = AuthUser.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user = User.objects.create(user_name='Тест', age=25, email='test@test.com')

    def test_list_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post('/api/users/', {
            'user_name': 'Новый', 'age': 20, 'email': 'new@test.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user_name'], 'Новый')

    def test_get_user(self):
        response = self.client.get(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        response = self.client.put(f'/api/users/{self.user.id}/', {
            'user_name': 'Обновлен', 'age': 30, 'email': 'updated@test.com'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        response = self.client.delete(f'/api/users/{self.user.id}/')
        self.assertEqual(response.status_code, 200)

    def test_patch_user(self):
        response = self.client.patch(f'/api/users/{self.user.id}/', {
            'age': 30
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['age'], 30)

    def test_user_posts(self):
        Post.objects.create(title='Пост юзера', author=self.user, body='Текст')
        response = self.client.get(f'/api/users/{self.user.id}/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_user_stats(self):
        response = self.client.get(f'/api/users/{self.user.id}/stats/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_posts', response.data)

    def test_create_user_without_auth(self):
        self.client.credentials()
        response = self.client.post('/api/users/', {
            'user_name': 'Без токена', 'age': 20, 'email': 'no@auth.com'
        })
        self.assertEqual(response.status_code, 401)


class PostTests(APITestCase):
    def setUp(self):
        self.auth_user = AuthUser.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user = User.objects.create(user_name='Автор', age=25, email='author@test.com')
        self.post = Post.objects.create(title='Тест пост', author=self.user, body='Тело поста')

    def test_list_posts(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post('/api/posts/', {
            'title': 'Новый пост', 'author': self.user.id, 'body': 'Текст'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Новый пост')

    def test_get_post(self):
        response = self.client.get(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_post(self):
        response = self.client.put(f'/api/posts/{self.post.id}/', {
            'title': 'Обновлен', 'author': self.user.id, 'body': 'Новый текст'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

    def test_patch_post(self):
        response = self.client.patch(f'/api/posts/{self.post.id}/', {
            'title': 'Новый заголовок'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Новый заголовок')

    def test_like_post(self):
        response = self.client.post(f'/api/posts/{self.post.id}/like/', {
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['liked'])

        response = self.client.post(f'/api/posts/{self.post.id}/like/', {
            'user_id': self.user.id
        })
        self.assertFalse(response.data['liked'])

    def test_post_comments(self):
        Comment.objects.create(author=self.user, post=self.post, body='Тестовый')
        response = self.client.get(f'/api/posts/{self.post.id}/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CommentTests(APITestCase):
    def setUp(self):
        self.auth_user = AuthUser.objects.create_user(username='admin', password='admin123')
        self.token = Token.objects.create(user=self.auth_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.user = User.objects.create(user_name='Автор', age=25, email='author@test.com')
        self.post = Post.objects.create(title='Пост', author=self.user, body='Текст')
        self.comment = Comment.objects.create(author=self.user, post=self.post, body='Комментарий')

    def test_list_comments(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        response = self.client.post('/api/comments/', {
            'author': self.user.id, 'post': self.post.id, 'body': 'Новый коммент'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], 'Новый коммент')

    def test_get_comment(self):
        response = self.client.get(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_update_comment(self):
        response = self.client.put(f'/api/comments/{self.comment.id}/', {
            'author': self.user.id, 'post': self.post.id, 'body': 'Обновлен'
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_comment(self):
        response = self.client.delete(f'/api/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)

    def test_patch_comment(self):
        response = self.client.patch(f'/api/comments/{self.comment.id}/', {
            'body': 'Обновленный'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['body'], 'Обновленный')

    def test_like_comment(self):
        response = self.client.post(f'/api/comments/{self.comment.id}/like/', {
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['liked'])

        response = self.client.post(f'/api/comments/{self.comment.id}/like/', {
            'user_id': self.user.id
        })
        self.assertFalse(response.data['liked'])
