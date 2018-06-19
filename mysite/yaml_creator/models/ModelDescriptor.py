from django.db import models
from django.utils import timezone
import re

# Create your models here.
def default_yaml_file_name():
    yaml_file_names=[m.filename for m in ModelDescriptor.objects.all()]
    
    # set a default file name for a new yaml file that is not already present
    default_trunk='default_'
    num_str='[0-9]+'
    P_num=re.compile(num_str)
    P=re.compile(default_trunk+num_str+'\.yaml')
    dl=[name for name in yaml_file_names if P.match(name) is not None]
    if len(dl)==0:
        yaml_file_name_default=default_trunk+'1.yaml'
    else:
        nmax=max([int(P_num.search(name).group()) for name in dl])
        yaml_file_name_default=default_trunk+str(nmax+1)+'.yaml'

    return yaml_file_name_default
###############################################

class ModelDescriptor(models.Model):
    filename=models.CharField(max_length=200,primary_key=True,default=default_yaml_file_name)
    doi=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')

