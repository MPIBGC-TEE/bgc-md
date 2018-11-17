from django.test import TestCase
from yaml_creator.models.Variable import Variable
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.StateVectorPosition import StateVectorPosition 
from django.db import transaction

#class VariableTest(TestCase):
#    def setUp(self)
#        m1=ModelDescriptor(folder_name='default_1')
#        m2=ModelDescriptor(folder_name='default_2')
#        m3=ModelDescriptor(folder_name='default_3')
for m in ModelDescriptor.objects.all():
    m.delete()

m1=ModelDescriptor(folder_name='default_1')
m1.save()
y=Variable(model_id=m1,symbol='y')
y.save()
# the next lines should create an exeption
#v2=Variable(model_id=m1,symbol='y')
#v2.save()
x=Variable(model_id=m1,symbol='x')
x.save()
k=Variable(model_id=m1,symbol='k')
k.save()
StateVectorPosition.objects.create(var_id=x,pos_id=0)
StateVectorPosition.objects.create(var_id=y,pos_id=1)
# now make a query to extract the Statevector for 'default_1'
[ v.symbol for v in Variable.objects.filter( statevectorposition__var_id__model_id="default_1").order_by('statevectorposition__pos_id') ]

