# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient, APITestCase

class RegisterViewTest(APITestCase):
    '''
    Class for testing the RegisterView
    '''
    def setUp(self):
        '''
        For all the tests we need to create a client
        '''
        self.client = APIClient()
    
    def test_register_user_success(self):
        '''
        Register a user is successful if the name, username and password are provided
        '''
        response = self.client.post('/user/register', {
            "name": "test",
            "username": "test_user",
            "password": "test_password"
        })
        
        self.assertContains(response, "jwt", status_code=200)
        
    def test_register_user_failure(self):
        '''
        Register a user is successful only if the name, username and password are provided
        '''
        response1 = self.client.post('/user/register', {
            "name": "test",
            "username": "test_user",
        })
        response2 = self.client.post('/user/register', {
            "username": "test_user",
            "password": "test_password"
        })
        response3 = self.client.post('/user/register', {
            "name": "test",
            "password": "test_password"
        })
        self.assertTrue(
            response1.status_code == 400 and 
            response2.status_code == 400 and 
            response3.status_code == 400
        )
        
    def test_register_user_repeated_failure(self):
        '''
        Register a user is successful if the username is not repeated
        '''
        self.client.post('/user/register', {
            "name": "test",
            "username": "test_user",
            "password": "test_password"
        })
        
        response_repeated = self.client.post('/user/register', {
            "name": "test",
            "username": "test_user",
            "password": "test_password"
        })
        self.assertContains(response_repeated, "username already exists", status_code=400)
