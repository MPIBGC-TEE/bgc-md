
from django.db import models
from django.core.exceptions import ValidationError
from .ModelDescriptor import ModelDescriptor
from .Variable import Variable

     
class StateVectorPosition(models.Model):
    var_id=models.ForeignKey(Variable,on_delete=models.CASCADE)
    pos_id=models.IntegerField(
            primary_key=True,
    )
    #description=models.CharField(max_length=200)
    #unit=models.CharField(max_length=200)

