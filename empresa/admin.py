
"""Admin configuration for the empresa app."""

from django.contrib import admin

from .models import Empresa  # Replace 'YourModelName' with your actual model class name

# Register your models here.
admin.site.register(Empresa)  # Register your model with the admin site
