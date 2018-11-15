from django.db import models
from . Variable import Variable

class InFlux(models.Model):
    expr=models.CharField(max_length=200)
    #since a pool can be the receipientp
    #we use the OneToOne relationship
    target=models.OneToOneField('Variable',on_delete=models.CASCADE)
