# Django
from django.db import models

# Local imports
from authentication_app.models import BaseModel, User

# Products app models (Bienes):
# - Product: name, description, user_id


class Product(BaseModel):
    '''
    Product class to represent a product:
    - name: the name of the product (Short description).
    - description: the description of the product (Long description).
    - user (FK): related to user id, on delete protect, default None.
    
    Called from User model as "products".
    '''
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name='products')