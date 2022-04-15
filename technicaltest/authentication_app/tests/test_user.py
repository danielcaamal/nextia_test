# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient, APITestCase

class UserViewTest(APITestCase):
    '''
    Class for testing User View
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
    
    def test_user_get(self):
        '''
        The user should be able to get the user information
        '''
        response = self.client.get(reverse('user'),)
        self.assertEqual(response.status_code, 200)
    
    def test_user_patch(self):
        '''
        The user should be able to update self information
        '''
        # Change password
        response = self.client.patch(reverse('user'), {
            "password": "test_password_2"
        })
        self.assertEqual(response.status_code, 200)
        
        # Logout
        self.client.post(reverse('user-logout'))
        
        # Login with new password
        response = self.client.post(reverse('user-login'), {
            "username": "test_user",
            "password": "test_password_2"
        })
        
        self.assertContains(response, "jwt", status_code=200)
    
    def test_user_delete(self):
        '''
        The user should be able to delete own account
        '''
        response = self.client.delete(reverse('user'))
        self.assertTrue(response.status_code == 204)