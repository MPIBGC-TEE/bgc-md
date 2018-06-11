from django.contrib import admin
# Register your models here.
from .models import ModelDescriptor

admin.site.register(ModelDescriptor)
