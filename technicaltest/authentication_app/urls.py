# Django
from django.urls import path, include

# Local imports
from authentication_app import views

# URL patterns for the users_app 
urlpatterns = [
    # user routes
    path('user', views.UserView.as_view(), name='user'),
    path('user/register', views.RegisterView.as_view(), name='user-register'),
    path('user/login', views.LoginView.as_view(), name='user-login'),
    path('user/logout', views.LogoutView.as_view(), name='user-logout'),
]