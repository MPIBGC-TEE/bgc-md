
from django.db import models
#from . ComponentScheme import ComponentScheme
class FluxRepresentation(models.Model):
    #componentscheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)
    @classmethod
    def get_subclassDict(cls):
        classes=cls.__subclasses__()
        return {c.__name__:c for c in classes}
        #or as an interator..
        #for subclass in cls.__subclasses__():
        #    yield from subclass.get_subclasses()
        #    yield subclass
    class Meta:
        abstract = True
