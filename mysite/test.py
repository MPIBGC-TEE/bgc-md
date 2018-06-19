from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.SingleFlux import SingleFlux
from yaml_creator.models.Variable import Variable
md=ModelDescriptor.objects.get(pk='default_1.yaml')
a=Variable.objects.create(name='a',model_descriptor=md)
b=Variable.objects.create(name='b',model_descriptor=md)
c=Variable.objects.create(name='c',model_descriptor=md)
ab=SingleFlux(source=a,target=b)
ac=SingleFlux(source=a,target=c)
bc=SingleFlux(source=b,target=c)
