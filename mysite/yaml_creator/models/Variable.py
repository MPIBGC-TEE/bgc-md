
from django.db import models
from django.core.exceptions import ValidationError
from .ModelDescriptor import ModelDescriptor

     
class Variable(models.Model):
    model_id=models.ForeignKey(ModelDescriptor,on_delete=models.CASCADE)
    symbol=models.CharField(
            max_length=200
    )
    #description=models.CharField(max_length=200)
    #unit=models.CharField(max_length=200)


    class Meta:
        # since django does not support primary keys consisting of 
        # two colums( in out casee model_id and symbol we fall back on the additional key id which is added by django per default 
        # and declare the model_id and symbol fields as unique_together
        unique_together=(('model_id','symbol'),)
