from django.db import models
from . Variable import Variable

class OutFlux(models.Model):
    #since a pool can be the donor of only one Outputflux 
    #we use the OneToOne relationship
    expr=models.CharField(max_length=200)
    source=models.OneToOneField('Variable',on_delete=models.CASCADE)
