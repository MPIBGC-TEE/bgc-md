from django.db import models
from django.utils import timezone

# Create your models here.

class ModelDescriptor(models.Model):
    name=models.CharField(max_length=200)
    doi=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')

class Variable(models.Model):
    name=models.CharField(max_length=200)
    model_descriptor=models.ForeignKey(ModelDescriptor,on_delete=models.CASCADE)
    reverse_execution_order_position=models.IntegerField(default=0)
