
#from django.shortcuts import render
import re
from string import Template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from pathlib import Path
from bgc_md.reports import defaults
from bgc_md.Model import Model
from bgc_md.component_schemes import  available_component_schemes
from yaml_creator.models import ModelDescriptor,ComponentScheme,FluxRepresentation,Fluxes
def index(request):
    ap=defaults()['paths']['data'].joinpath('all_records')
    print(ap)
    yaml_file_names=[p.name for p in ap.iterdir()]
    
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

    context={
        'yaml_file_names':yaml_file_names,
        'yaml_file_name_default':yaml_file_name_default
    }

    #template=loader.get_template('yaml_creator/index.html')
    #return HttpResponse(template.render(context,request))
    return render(request,'yaml_creator/index.html',context)
