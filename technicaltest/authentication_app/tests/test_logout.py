# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient, APITestCase


class Logout(APITestCase):
    '''
    Class for testing the LogoutView
    '''
    def setUp(self):
        '''
        For all the tests we need to create a client and register(login) a user to logout
        '''
        self.client = APIClient()
        self.client.post(reverse('user-register'), {
            "name": "test",
            "username": "test_user",
            "password": "test_password"
        })
    
    def test_logout_user_success(self):
        self.client.post(reverse('user-login'), {
            "username": "test_user",
            "password": "test_password"
        })
        response = self.client.post(reverse('user-logout'),)
        self.assertContains(response, "Logged out", status_code=200)

    def test_logout_user_already_logout(self):
        self.client.post(reverse('user-login'), {
            "username": "test_user",
            "password": "test_password"
        })
        self.client.post(reverse('user-logout'),)
        response = self.client.post(reverse('user-logout'),)
        self.assertContains(response, "Already logged out", status_code=200)