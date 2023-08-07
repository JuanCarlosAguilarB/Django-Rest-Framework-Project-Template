# Django
from django.test import TestCase

# Python
from PIL import Image
import tempfile
import json

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status

# Models
from apps.user.models import User


from django.contrib.auth.hashers import make_password


class UserTestCase(TestCase):

    def setUp(self):
        user = User(
            email='admin@gmail.com',
            first_name='Testing',
            last_name='Testing',
            username='testing_login'
        )
        user.set_password('F12345678@')
        user.save()

    def test_signup_UserAuth(self):
        """Check if we can create an user"""

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        client = APIClient()
        response = client.post(
            '/api/v1/users/signup/', {
                'email': 'testing@cosasdedevs.com',
                'password': 'rc{4@qHjR>!b`yAV',
                'password2': 'rc{4@qHjR>!b`yAV',
                'first_name': 'Testing',
                'last_name': 'Testing',
                'phone': '999888777',
                # 'city': 'Madrid',
                # 'country': 'España',
                'photo': tmp_file,
                'username': 'testing1'
            },
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_info = json.loads(response.content)
        self.assertEqual(user_info['email'], "testing@cosasdedevs.com")
        # self.assertEqual(user_info['password'], make_password('rc{4@qHjR>!b`yAV'))
        self.assertEqual(user_info['first_name'], "Testing")
        self.assertEqual(user_info['last_name'], "Testing")
        self.assertEqual(user_info['phone'], "999888777")
        self.assertEqual(user_info['username'], "testing1")

    def test_login_UserAuth(self):
        """Check if we can log in the page"""

        client = APIClient()
        response = client.post(
            '/login', {
                'email': 'admin@gmail.com',
                'password': 'F12345678@',
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = json.loads(response.content)
        self.assertIn('access', result)
