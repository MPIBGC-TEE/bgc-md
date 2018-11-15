
from django.db import models
from django.core.exceptions import ValidationError
from .ModelDescriptor import ModelDescriptor

     
class Variable(models.Model):
    model_id=models.ForeignKey(ModelDescriptor,on_delete=models.CASCADE)
    symbol=models.CharField(
            max_length=200,
            primary_key=True,
    )
    #description=models.CharField(max_length=200)
    #unit=models.CharField(max_length=200)
