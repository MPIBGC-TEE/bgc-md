from django.db import models
from . Variable import Variable

#class SingleFlux(models.Model):
class InternalFlux(models.Model):
    expr=models.CharField(max_length=200)
    source=models.ForeignKey('Variable',related_name='donating',on_delete=models.CASCADE)
    target=models.ForeignKey('Variable',related_name='receiving',on_delete=models.CASCADE)
