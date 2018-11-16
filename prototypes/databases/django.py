from django.test import TestCase
from yaml_creator.models.Variables import Variable
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from django.db import transaction

#class VariableTest(TestCase):
#    def setUp(self)
#        m1=ModelDescriptor(folder_name='default_1')
#        m2=ModelDescriptor(folder_name='default_2')
#        m3=ModelDescriptor(folder_name='default_3')

m1=ModelDescriptor(folder_name='default_1')
m1.save()
v1=Variable(model_id=m1,symbol='x')
v1.save()
v2=Variable(model_id=m1,symbol='x')
# the next lines should create an exeption
v2.save()
#v2=Variable(model_id=m1,symbol='y')
#v3=Variable(model_id=m1,symbol='z')
#@transaction.atomic
#def storeModel(folder_name:str,variable_list:list):
#    m=ModelDescriptor(folder_name='default_1')
#    m.save()
#    for i,v in Variable_list: 
#        v=Variable(model_id=m,symbol=v)
#        v.save()
##with transaction.atomic()
##    m=ModelDescriptor(folder_name='default_2')
#storeModel(folder_name='default_1',variable_list=['x','y','z']
