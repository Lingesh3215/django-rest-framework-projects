from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import UserModel, RoleModel, NewsModel
from rest_framework_simplejwt.tokens import RefreshToken

class NewsAggregatorTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.reporter_role = RoleModel.objects.create(role_name='reporter')
        self.user_role = RoleModel.objects.create(role_name='user')

        self.reporter = UserModel.objects.create_user(
            username='reporter1', email='reporter@example.com',
            password='testpass123', role=self.reporter_role
        )
        self.user = UserModel.objects.create_user(
            username='user1', email='user@example.com',
            password='testpass123', role=self.user_role
        )

        # Generate JWTs
        self.reporter_token = str(RefreshToken.for_user(self.reporter).access_token)
        self.user_token = str(RefreshToken.for_user(self.user).access_token)

        self.news_data = {
            "title": "Breaking News",
            "content": "Important update...",
            "category": "world"
        }

    # LOGIN TESTS (3)
    def test01_login_success(self):
        res = self.client.post('/login/', {"email": "user@example.com", "password": "testpass123"})
        self.assertEqual(res.status_code, 201)

    def test2_login_missing_fields(self):
        res = self.client.post('/login/', {"email": "user@example.com"})
        self.assertEqual(res.status_code, 400)

    def test3_login_wrong_credentials(self):
        res = self.client.post('/login/', {"email": "user@example.com", "password": "wrong"})
        self.assertEqual(res.status_code, 401)

    # POST NEWS TESTS (3)
    def test4_post_news_by_reporter_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        res = self.client.post('/news/', self.news_data)
        self.assertEqual(res.status_code, 201)

    def test5_post_news_missing_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        invalid_data = {**self.news_data}
        del invalid_data["category"]
        res = self.client.post('/news/', invalid_data)
        self.assertEqual(res.status_code, 400)

    def test6_post_news_by_non_reporter(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        res = self.client.post('/news/', self.news_data)
        self.assertEqual(res.status_code, 403)

    # LIST NEWS TESTS (3)
    def test7_list_news_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        NewsModel.objects.create(**self.news_data, author=self.reporter)
        NewsModel.objects.create(title="Another", content="Extra", category="world", author=self.reporter)
        res = self.client.get('/news/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 2)

    def test8_list_news_unauthenticated(self):
        res = self.client.get('/news/')
        self.assertEqual(res.status_code, 401)

    def test9_list_news_empty_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        res = self.client.get('/news/?category=printer')
        self.assertEqual(res.status_code, 200)  # Adjust to match actual response
        self.assertEqual(len(res.data), 0)

    # UPDATE NEWS TESTS (3)
    def test10_update_news_by_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.put(f'/news/{news.id}/', {"title": "Updated", "content": "Changed", "category": "world"})
        self.assertEqual(res.status_code, 200)

    def test11_update_news_by_non_author(self):
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        res = self.client.put(f'/news/{news.id}/', {"title": "Illegal", "content": "Denied", "category": "tech"})
        self.assertEqual(res.status_code, 403)

    def test12_update_news_invalid_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        res = self.client.put('/news/999/', {"title": "Oops", "content": "Lost", "category": "world"})
        self.assertEqual(res.status_code, 404)

    # DELETE NEWS TESTS (3)
    def test13_delete_news_by_author(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.delete(f'/news/{news.id}/')
        self.assertEqual(res.status_code, 204)

    def test14_delete_news_by_non_author(self):
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        res = self.client.delete(f'/news/{news.id}/')
        self.assertEqual(res.status_code, 403)

    def test15_delete_news_invalid_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        res = self.client.delete('/news/999/')
        self.assertEqual(res.status_code, 404)


    # AUTHENTICATION EDGE CASES
    def test16_login_with_blank_password(self):
        res = self.client.post('/login/', {"email": "user@example.com", "password": ""})
        self.assertEqual(res.status_code, 400)

    def test17_login_with_nonexistent_email(self):
        res = self.client.post('/login/', {"email": "ghost@example.com", "password": "testpass123"})
        self.assertEqual(res.status_code, 400)

    def test18_access_news_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken123')
        res = self.client.get('/news/')
        self.assertEqual(res.status_code, 401)

    # NEWS CREATION VALIDATION
    def test19_post_news_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        invalid_data = {"content": "No title", "category": "world"}
        res = self.client.post('/news/', invalid_data)
        self.assertEqual(res.status_code, 400)

    def test20_post_news_with_empty_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        empty_data = {"title": "", "content": "", "category": ""}
        res = self.client.post('/news/', empty_data)
        self.assertEqual(res.status_code, 400)

    # FILTERING & QUERY PARAMS
    def test21_list_news_by_valid_category(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.get('/news/?category=world')
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test22_list_news_by_invalid_query_param(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        res = self.client.get('/news/?unknown=xyz')
        self.assertEqual(res.status_code, 200)

    # UPDATE EDGE CASES
    def test23_update_news_with_partial_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.patch(f'/news/{news.id}/', {"title": "Partial Update"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["title"], "Partial Update")

    def test24_update_news_with_empty_payload(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.put(f'/news/{news.id}/', {})
        self.assertEqual(res.status_code, 400)

    # DELETE EDGE CASES
    def test25_delete_news_twice(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.reporter_token}')
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res1 = self.client.delete(f'/news/{news.id}/')
        res2 = self.client.delete(f'/news/{news.id}/')
        self.assertEqual(res1.status_code, 204)
        self.assertEqual(res2.status_code, 404)

    def test26_delete_news_without_authentication(self):
        news = NewsModel.objects.create(**self.news_data, author=self.reporter)
        res = self.client.delete(f'/news/{news.id}/')
        self.assertEqual(res.status_code, 401)
