# Python
import datetime
import jwt
import os

# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

# Local imports
from authentication_app.models import User


# Function to generate jwt token
def generate_jwt_token(user: User):
    '''
    Function to generate jwt token
    
    Args:
        user: the user to generate the token
    
    Returns:
        Object Response with the token as cookie
    '''
    
    # Generate the token
    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, os.environ.get("SECRET_KEY", default='SECRET_KEY'), algorithm='HS256').decode('utf-8')
    
    # Setting the response
    response = Response()
    response.data = {
        'jwt': token
    }
    
    # Setting the cookie (Only accessed by the backend)
    response.set_cookie(key='jwt', value=token, httponly=True)
    
    # Return the authentication token
    return response


# Function to check if the user is authenticated
def check_authentication(request):
    '''
    Function to check the authentication of the user
    
    Args:
        - request: the request to check the authentication
    
    Returns:
        - user: the user if the user is authenticated, else raise an exception
    '''
    # Valdate the token
    token = request.COOKIES.get('jwt', None)
    
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    
    # Decode the token, if not valid raise an exception
    payload = None
    try:
        payload = jwt.decode(token, os.environ.get("SECRET_KEY", default='SECRET_KEY'), algorithms=['HS256'])
    except Exception as err:
        raise AuthenticationFailed('Unauthenticated')
    
    # Get the user by id or raise an exception
    user = get_object_or_404(User, pk=payload['id'])
    return user