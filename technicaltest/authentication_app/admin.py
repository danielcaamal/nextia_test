# Django
from django.contrib import admin

# Local imports
from authentication_app.models import User

# Register User in admin site
admin.site.register(User)