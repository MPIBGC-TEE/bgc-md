from django.core.exceptions import ObjectDoesNotExist,ValidationError
from django.utils import timezone
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.Fluxes import Fluxes
from yaml_creator.models.Matrices import Matrices
from yaml_creator.models.SingleFlux import SingleFlux
from yaml_creator.models.Variable import Variable
modelName="testModel"
try:
    md=ModelDescriptor.objects.get(pk=modelName)
    md.delete()
except ObjectDoesNotExist:
    md=ModelDescriptor.objects.create(pk=modelName,pub_date=timezone.now())
    md.save()
for var in Variable.objects.all():
    var.delete()
print(md)
md.save()
sv="Matrix([a,b,c]"
cs=ComponentScheme(model_descriptor=md,statevector=sv)
cs.save()
a=Variable.objects.create(name='a',model_descriptor=md)
b=Variable.objects.create(name='b',model_descriptor=md)
c=Variable.objects.create(name='c',model_descriptor=md)
#fr=Fluxes(componentScheme=cs)
fr=Matrices(componentScheme=cs)
ab=SingleFlux(source=a,target=b)
ab.save()
ac=SingleFlux(source=a,target=c)
ac.save()
bc=SingleFlux(source=b,target=c)
bc.save()
print(a.donating.all())


