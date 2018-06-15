
from . ModelDescriptor import ModelDescriptor
from django.db import models
class ComponentScheme(models.Model):
    #model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    model_descriptor=models.OneToOneField('ModelDescriptor',on_delete=models.CASCADE)
    stateVector=models.CharField(max_length=200)
    #fluxrep=models.OneToOneField(FluxRepresentation,on_delete=models.CASCADE,primary_key=True)

