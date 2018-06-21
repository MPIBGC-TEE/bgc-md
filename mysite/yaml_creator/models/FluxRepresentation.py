
from django.db import models
from . ComponentScheme import ComponentScheme
class FluxRepresentation(models.Model):
    componentScheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)
    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass
