from django.db import models
from . Variable import Variable

#class SingleFlux(models.Model):
class SingleFlux(models.Model):
    expr=models.CharField(max_length=200)
    source=models.ForeignKey('Variable',related_name='source',on_delete=models.CASCADE)
    target=models.ForeignKey('Variable',related_name='target',on_delete=models.CASCADE)
