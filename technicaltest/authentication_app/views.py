# Django
from django.contrib.auth.hashers import check_password

# Django REST Framework
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

# Local imports
from authentication_app.models import User
from authentication_app.serializers import UserSerializer
from authentication_app.services import check_authentication, generate_jwt_token


### Authentication Views ###
class RegisterView(APIView):
    def post(self, request):
        # Get the data from the request and serialize it
        serializer = UserSerializer(data=request.data)
        
        # Check if the data is valid or raise an exception
        serializer.is_valid(raise_exception=True)
        
        # Save the data in the database
        user = serializer.save()
        
        # Generate the token (Create JWT after registering)
        response = generate_jwt_token(user)
        
        # Return the response
        return response


class LoginView(APIView):
    def post(self, request):
        # Get the data from the request and serialize it
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        
        # Get the user by username
        user = User.objects.filter(username=username).first()
        
        # Raise an exception if the user doesn't exist
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        
        # Comparing the password (password, hashed_password)
        if not check_password(password, user.password):
            raise AuthenticationFailed('Invalid credentials')
            
        # Generate the JWT token
        response = generate_jwt_token(user)
        
        # Return the response
        return response


class LogoutView(APIView):
    def post(self, request):
        # Delete the cookie
        response = Response()
        
        # Getting the cookie
        token = request.COOKIES.get('jwt', None)
        
        # Deleting the cookie if exists and seeting message in the response
        if token:
            response.delete_cookie('jwt')
            response.data = {'message': 'Logged out'}
        else:
            response.data = {'message': 'Already logged out'}
        
        # Return the response
        return response


### User Views ###
class UserView(APIView):
    # Obtain the user logged in
    def get(self, request):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Serialize the user
        serializer = UserSerializer(user)
        
        # Return the user
        return Response(serializer.data)
    
    # Update the user logged in
    def patch(self, request):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Get the data from the request and serialize it
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        # Check if the data is valid or raise an exception
        serializer.is_valid(raise_exception=True)
        
        # Update the user
        serializer.save()
        
        # Return the updated user
        return Response(serializer.data)
    
    # Delete the user logged in
    def delete(self, request):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Delete the user
        user.delete()
        
        # Return message in the response
        return Response({'message': 'User deleted'})