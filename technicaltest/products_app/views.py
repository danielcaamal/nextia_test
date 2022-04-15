# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

# Local imports
from authentication_app.services import check_authentication
from products_app.serializers import ProductSerializer


### Products Views ###
class ProductsView(APIView):
    # List the products given ids
    def get(self, request):
        # Check JWT authentication
        user = check_authentication(request)
                
        # Obtaining the ids
        ids = request.query_params.getlist('id')
        
        if ids:
            # Return the products given ids
            products = user.products.filter(id__in=ids).order_by('id')
        else:
            # Return all the user's products
            products = user.products.all()
        
        # Serialize the products
        serializer = ProductSerializer(products, many=True)
        
        # Return the products
        return Response(serializer.data)
    
    # Create Product
    def post(self, request):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Serialize the request data
        serializer = ProductSerializer(data=request.data)
        
        # Validate the request data
        serializer.is_valid(raise_exception=True)
        
        # Create the product
        serializer.save(user=user)
        
        # Return the created product
        return Response(serializer.data, status=status.HTTP_201_CREATED)



### Product Detail Views ###
class ProductsDetailView(APIView):
    # Read the product
    def get(self, request, pk):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Get the product
        product = get_object_or_404(user.products, id=pk)
        
        # Serialize the product
        serializer = ProductSerializer(product)
        
        # Return the user product
        return Response(serializer.data)
    
    # Update the product
    def patch(self, request, pk):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Get the product
        product = get_object_or_404(user.products, id=pk)
        
        # Serialize the request data
        serializer = ProductSerializer(product, data=request.data, partial=True)
        
        # Validate the request data
        serializer.is_valid(raise_exception=True)
        
        # Update the product
        serializer.save()
        
        # Return the updated product
        return Response(serializer.data)
    
    # Delete the product
    def delete(self, request, pk):
        # Check JWT authentication
        user = check_authentication(request)
        
        # Get the product
        product = get_object_or_404(user.products, id=pk)
        
        # Delete the product
        product.delete()
        
        # Return the user
        return Response({}, status=status.HTTP_204_NO_CONTENT)