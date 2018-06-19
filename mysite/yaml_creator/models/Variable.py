from django.db import models
from .ModelDescriptor import ModelDescriptor

def clean(self):
    #we want variable names unique in a model_descriptor
    pass
     
class Variable(models.Model):
    name=models.CharField(max_length=200)

    model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    reverse_execution_order_position=models.IntegerField(default=0)

