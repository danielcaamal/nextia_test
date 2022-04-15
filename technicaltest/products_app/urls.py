# Django
from django.urls import path, include

# Local imports
from products_app import views

# URL patterns for the users_app 
urlpatterns = [
    # product routes
    path('product', views.ProductsView.as_view(), name='product'),
    path('product/<int:pk>', views.ProductsDetailView.as_view(), name='product-detail'),
]