# Django
from django.db import models

# Authentication app models:
# - BaseModel: id, created_at, updated_at
# - User: name, username, password


class BaseModel(models.Model):
    '''
    BaseModel class for all models:
    - id: is the primary key of the models.
    - created_at and updated_at: are auto_now_add and auto_now
        for the creation and update fields of the model to manage
        the time of the modifications.
    '''
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        abstract = True


class User(BaseModel):
    '''
    User class to represent a user:
    - name: the name of the user.
    - username: the username of the user (This is unique).
    - password: the password of the user.
    
    All the fields are required.
    '''
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)