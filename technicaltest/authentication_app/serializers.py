# Django
from django.contrib.auth.hashers import make_password

# Django REST Framework
from rest_framework import serializers

# Local imports
from authentication_app.models import User

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Setting the model
        model = User
        
        # Fields to be included in the serializer
        fields = ['id', 'name', 'username', 'password']
        
        # Fields to be required
        required = ['name', 'username', 'password']
        
        # Make the password only writable
        extra_kwargs = {'password': {'write_only': True}}
        
    # Override the create method for password hashing
    def create(self, validated_data):
        # Getting the password from the validated data
        password = validated_data.pop('password', None)
        
        # Instantiating the user
        instance = self.Meta.model(**validated_data)
        
        # Password validation
        if password is not None:
            # Making the password hashable (default password hasher)
            instance.password = make_password(password)
        
        # Saving the user
        instance.save()
        
        # Returning the instance
        return instance
    
    # Override the update method for password hashing
    def update(self, instance, validated_data):
        # Getting the password from the validated data
        password = validated_data.pop('password', None)
        print(validated_data)
        
        # Password validation
        if password is not None:
            # Making the password hashable (default password hasher)
            instance.password = make_password(password)
        
        # Updating the instance user
        instance.__dict__.update(**validated_data)
        
        # Saving the user
        instance.save()
        
        # Returning the instance
        return instance