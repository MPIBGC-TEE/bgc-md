from django.db import models
from . ComponentScheme import ComponentScheme

class FluxDict(models.Model):
    fluxes=models.CharField(max_length=200)
    color=models.CharField(max_length=200,default='red')
    #componentScheme=models.ForeignKey('ComponentScheme',on_delete=models.CASCADE)
    componentScheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)
