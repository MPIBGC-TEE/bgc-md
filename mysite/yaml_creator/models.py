from django.db import models
from django.utils import timezone
import re
from bgc_md.reports import defaults

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
##############################################


class Variable(models.Model):
    name=models.CharField(max_length=200)
    model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    reverse_execution_order_position=models.IntegerField(default=0)

class FluxRepresentation(models.Model):
    componentScheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)
    @classmethod
    def get_subclasses(cls):
        for subclass in cls.__subclasses__():
            yield from subclass.get_subclasses()
            yield subclass


class ComponentScheme(models.Model):
    #model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    model_descriptor=models.OneToOneField('ModelDescriptor',on_delete=models.CASCADE)
    stateVector=models.CharField(max_length=200)
    #fluxrep=models.OneToOneField(FluxRepresentation,on_delete=models.CASCADE,primary_key=True)

class CompartmentalMatrixAndInputVec(FluxRepresentation):
    A=models.CharField(max_length=2000)

class Fluxes(FluxRepresentation):
    pass

class FluxDict(models.Model):
    fluxes=models.CharField(max_length=200)
    color=models.CharField(max_length=200,default='red')
    #componentScheme=models.ForeignKey('ComponentScheme',on_delete=models.CASCADE)
    componentScheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)

class ModelDescriptor(models.Model):
    filename=models.CharField(max_length=200,primary_key=True,default=default_yaml_file_name)
    doi=models.CharField(max_length=200)
    pub_date=models.DateTimeField('date published')

    @classmethod
    def default_yaml_file_name(cls):
        yaml_file_names=[m.filename for m in cls.objects.all()]
        
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
