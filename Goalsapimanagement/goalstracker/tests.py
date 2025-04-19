from django.test import TestCase, Client
from .models import DailyGoal
import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class DailyGoalTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.auth_header = f'Bearer {self.access_token}'
        self.goal = DailyGoal.objects.create(
            title="Morning Exercise",
            description="30 mins walk",
            category="Health",
            priority="High",
            is_completed=False
        )
        self.valid_payload = {
            "title": "Read Book",
            "description": "Read 20 pages of a novel",
            "category": "Personal",
            "priority": "Medium",
            "is_completed": False
        }

    def test_create_goal_should_return_201_and_create_object(self):
        response = self.client.post(
            '/goals',
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 201, "Expected status code 201")
        self.assertEqual(DailyGoal.objects.count(), 2)
        data = response.json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], self.valid_payload['title'])

    def test_list_goals_should_return_200_and_contain_existing_data(self):
        response = self.client.get(
            '/goals',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('title', data[0])
        self.assertEqual(data[0]['title'], self.goal.title)

    def test_get_goal_should_return_200_and_correct_data(self):
        response = self.client.get(
            f'/goals/{self.goal.id}',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], self.goal.title)
        self.assertEqual(data['category'], self.goal.category)

    def test_update_goal_should_return_200_and_modify_data(self):
        update_data = {
            "title": "Updated Goal",
            "description": "Updated description",
            "category": "Work",
            "priority": "Low",
            "is_completed": True
        }
        response = self.client.patch(
            f'/goals/{self.goal.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], "Updated Goal")
        self.goal.refresh_from_db()
        self.assertEqual(self.goal.description, "Updated description")

    def test_delete_goal_should_return_204_and_delete_object(self):
        response = self.client.delete(
            f'/goals/{self.goal.id}',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(DailyGoal.objects.filter(id=self.goal.id).exists())

    def test_get_invalid_goal_should_return_404_and_error_message(self):
        response = self.client.get(
            '/goals/999',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", response.content.decode())

    def test_delete_invalid_goal_should_return_404(self):
        response = self.client.delete(
            '/goals/999',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Not found", response.content.decode())

    def test_create_invalid_goal_should_return_400(self):
        invalid_payload = {
            "title": "",
            "description": "No title here",
            "category": "General",
            "priority": "Low",
            "is_completed": False
        }
        response = self.client.post(
            '/goals',
            data=json.dumps(invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.content.decode())

    def test_update_invalid_goal_should_return_400(self):
        invalid_payload = {
            "title": "",
            "description": "Invalid update",
            "category": "General",
            "priority": "Low",
            "is_completed": False
        }
        response = self.client.patch(
            f'/goals/{self.goal.id}',
            data=json.dumps(invalid_payload),
            content_type='application/json',
            HTTP_AUTHORIZATION=self.auth_header  # Include JWT token
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.content.decode())


class JWTGoalTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.goal = DailyGoal.objects.create(
            title="Morning Exercise",
            description="30 mins walk",
            category="Health",
            priority="High",
            is_completed=False
        )
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.auth_header = f'Bearer {self.access_token}'
        self.valid_payload = {
            "title": "Read Book",
            "description": "Read 20 pages of a novel",
            "category": "Personal",
            "priority": "Medium",
            "is_completed": False
        }

    def test_create_goal_without_jwt_should_fail(self):
        response = self.client.post('/goals', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_create_goal_with_jwt_should_succeed(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.post('/goals', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)

    def test_list_goals_requires_jwt(self):
        response = self.client.get('/goals')
        self.assertEqual(response.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.get('/goals')
        self.assertEqual(response.status_code, 200)

    def test_update_goal_requires_jwt(self):
        update_data = {"title": "Updated", "description": "Updated", "category": "Work", "priority": "Low", "is_completed": True}
        response = self.client.patch(f'/goals/{self.goal.id}', update_data, format='json')
        self.assertEqual(response.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.patch(f'/goals/{self.goal.id}', update_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_goal_requires_jwt(self):
        response = self.client.delete(f'/goals/{self.goal.id}')
        self.assertEqual(response.status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        response = self.client.delete(f'/goals/{self.goal.id}')
        self.assertEqual(response.status_code, 204)
