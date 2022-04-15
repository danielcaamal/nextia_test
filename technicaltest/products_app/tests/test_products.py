# Django
from django.test import TestCase
from django.urls import reverse

# Django REST Framework
from rest_framework.test import APIClient, APITestCase

class ProductViewTest(APITestCase):
    '''
    Class for testing Product Views
    '''
    def setUp(self):
        '''
        For all the tests we need to create a client and register(login)
        for the register and test the products views (it needs JWT authentication)
        The user information is returned in every type of request
        '''
        self.client = APIClient()
        self.user_name = 'test'
        self.client.post(reverse('user-register'), {
            "name": self.user_name,
            "username": "test_user",
            "password": "test_password"
        })
    
    def test_products_post(self):
        '''
        The user should be able to create a product
        '''
        response = self.client.post(reverse('product'), {
            "name": "Xbox S renew",
            "description": "Xbox renewed on April 2022",
        })
        self.assertTrue(
            response.status_code == 201 and 
            response.data['user']['name'] == self.user_name
        )
        
    def test_products_list(self):
        '''
        The user should be able to see own products
        '''
        product1 = "PS4 controller"
        product2 = "Keyboard ASUS"
        # Creating products
        self.client.post(reverse('product'), {
            "name": product1,
            "description": "Controller for PS4",
        })
        
        self.client.post(reverse('product'), {
            "name": product2,
            "description": "RGB keyboard",
        })
        response = self.client.get(reverse('product'))
        self.assertTrue(
            len(response.data) == 2 and
            response.data[0]['user']['name'] == self.user_name
        )

    # @test.skip
    def test_products_get_by_ids(self):
        '''
        The user should be able to see own products by id list
        '''
        product1 = "PS4 controller 2"
        product2 = "Keyboard ASUS 2"
        product3 = "PC Gamer 2"
        # Creating products
        response = self.client.post(reverse('product'), {
            "name": product1,
            "description": "Controller for PS4",
        })
        id_1 = response.data['id']

        response = self.client.post(reverse('product'), {
            "name": product2,
            "description": "RGB keyboard",
        })
        id_2 = response.data['id']

        response = self.client.post(reverse('product'), {
            "name": product3,
            "description": "PC Gamer all included",
        })
        id_3 = response.data['id']
        
        # Getting only the posts with id 1 and 3
        response = self.client.get(reverse('product') + '?id={}&id={}'.format(id_1, id_3))
        self.assertTrue(
            len(response.data) == 2 and 
            response.data[0]['name'] == product1 and
            response.data[1]['name'] == product3 and 
            response.data[0]['user']['name'] == self.user_name
        )
    
    def test_products_get(self):
        name = "Xbox S renew"
        response = self.client.post(reverse('product'), {
            "name": name,
            "description": "Xbox renewed on April 2022",
        })
        pk = response.data['id']
        response = self.client.get(reverse('product-detail', args=[pk]))
        self.assertTrue(
            response.data['name'] == name and
            response.data['user']['name'] == self.user_name
        )
    
    def test_no_products_get(self):
        '''
        If not products are found, the user should be able to see 404 message
        '''
        pk = 1
        response = self.client.get(reverse('product-detail', args=[pk]))
        self.assertTrue(response.status_code, 404)
    
    
    def test_products_patch(self):
        '''
        The user should be able to update own products
        '''
        old_name = "Xbox S renew"
        new_name = "Xbox S new"
        response = self.client.post(reverse('product'), {
            "name": old_name,
            "description": "Xbox renewed on April 2022",
        })
        pk = response.data['id']
        response = self.client.patch(reverse('product-detail', args=[pk]), data ={
            "name": new_name,
        })
        self.assertTrue(
            response.data['name'] == new_name and
            response.data['user']['name'] == self.user_name
        )
        
    def test_user_delete(self):
        '''
        The user should be able to delete own products
        '''
        name = "Xbox S renew"
        response = self.client.post(reverse('product'), {
            "name": name,
            "description": "Xbox renewed on April 2022",
        })
        pk = response.data['id']
        response = self.client.delete(reverse('product-detail', args=[pk]))
        self.assertTrue(response.status_code == 204)