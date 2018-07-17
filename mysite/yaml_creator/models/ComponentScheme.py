
from . ModelDescriptor import ModelDescriptor
from django.db import models
class ComponentScheme(models.Model):
    model_descriptor=models.OneToOneField('ModelDescriptor',on_delete=models.CASCADE)
