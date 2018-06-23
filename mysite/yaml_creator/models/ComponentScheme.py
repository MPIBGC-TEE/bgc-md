
from . ModelDescriptor import ModelDescriptor
from django.db import models
class ComponentScheme(models.Model):
    model_descriptor=models.OneToOneField('ModelDescriptor',on_delete=models.CASCADE)
    statevector=models.CharField(max_length=200)
    #fluxrep=models.OneToOneField(FluxRepresentation,on_delete=models.CASCADE,primary_key=True)

