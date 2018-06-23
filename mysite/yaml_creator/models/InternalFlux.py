from django.db import models
from . Variable import Variable

#class SingleFlux(models.Model):
class InternalFlux(models.Model):
    expr=models.CharField(max_length=200)
    fluxes=models.ForeignKey('Fluxes',on_delete=models.CASCADE)
    #target=models.ForeignKey('Variable',related_name='receiving',on_delete=models.CASCADE)
    source=models.CharField(max_length=200,default='')
    target=models.CharField(max_length=200,default='')
