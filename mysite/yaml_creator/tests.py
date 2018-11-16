from django.test import TestCase
import unittest
from django.db.utils import IntegrityError
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.Variable import Variable
from yaml_creator.models.StateVectorPosition import StateVectorPosition 

# Create your tests here.
class VariableTest(TestCase):
    def setUp(self):
        m=ModelDescriptor(folder_name='default_1')
        m.save()
        Variable.objects.create(model_id=m,symbol='x')
        Variable.objects.create(model_id=m,symbol='y')

    def test_uniqueness_of_Variables_per_Model(self):
        m=ModelDescriptor.objects.filter(folder_name='default_1')[0]
        v1=Variable(model_id=m,symbol='s')
        v1.save()
        v2=Variable(model_id=m,symbol='s')
        with self.assertRaises(IntegrityError) as cm:
            v2.save()
        print(cm)
    
    #@unittest.skip('')
    def test_statevector(self):
        #m=ModelDescriptor.objects.filter(folder_name='default_0')[0]
        x=Variable.objects.get(model_id='default_1',symbol='x')
        y=Variable.objects.get(model_id='default_1',symbol='y')
        StateVectorPosition.objects.create(var_id=x,pos_id=0)
        StateVectorPosition.objects.create(var_id=y,pos_id=1)
        
