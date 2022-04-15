# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient, APITestCase


class LoginViewTest(APITestCase):
    '''
    Class for testing the LoginView
    '''
    def setUp(self):
        '''
        For all the tests we need to create a client and register a user
        '''
        self.client = APIClient()
        self.client.post(reverse('user-register'), {
            "name": "test",
            "username": "test_user",
            "password": "test_password"
        })
    
    def test_login_user_success(self):
        '''
        Login a user is successful if the username and password are provided and the user is registered
        '''
        response = self.client.post(reverse('user-login'), {
            "username": "test_user",
            "password": "test_password"
        })
        self.assertContains(response, "jwt", status_code=200)
        
    def test_login_user_failure(self):
        '''
        Login user is failed if the username or password are not correct or if the user is not registered
        '''
        response1 = self.client.post(reverse('user-login'), {
            "username": "test_user",
            "password": "test_password2"
        })
        
        response2 = self.client.post(reverse('user-login'), {
            "username": "test_user2",
            "password": "test_password"
        })        
        self.assertTrue(
            response1.status_code == 403 and
            response2.status_code == 403             
        )