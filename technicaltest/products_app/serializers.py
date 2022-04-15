# Django REST Framework
from rest_framework import serializers

# Local imports
from authentication_app.serializers import UserSerializer
from products_app.models import Product

# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    # Populate the user field with the user id
    user = UserSerializer(read_only=True)
    
    class Meta:
        # Setting the model
        model = Product
        
        # Fields to be included in the serializer
        fields = ['id', 'name', 'description', 'user']
        
        # Fields to be required
        required = ['name']