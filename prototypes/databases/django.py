
from yaml_creator.models.Variables import Variable
from yaml_creator.models.ModelDescriptor import ModelDescriptor
m1=ModelDescriptor(folder_name='default_1')
m2=ModelDescriptor(folder_name='default_2')
m3=ModelDescriptor(folder_name='default_3')
v1=Variable(model_id=m1,symbol='x')
# the next two lines should not be possible
v2=Variable(model_id=m1,symbol='x')
v2=Variable(model_id=m1,symbol='x')
