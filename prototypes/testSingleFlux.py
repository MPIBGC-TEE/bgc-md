from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.SingleFlux import SingleFlux
from yaml_creator.models.Variable import Variable
md=ModelDescriptor.objects.get(pk='default_1.yaml')
a=Variable.objects.create(name='a',model_descriptor=md)
a.save()
b=Variable.objects.create(name='b',model_descriptor=md)
b.save()
c=Variable.objects.create(name='c',model_descriptor=md)
c.save()
ab=SingleFlux(source=a,target=b)
ab.save()
ac=SingleFlux(source=a,target=c)
ac.save()
bc=SingleFlux(source=b,target=c)
bc.save()
print(a.donating.all())

