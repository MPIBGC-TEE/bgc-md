#from django.shortcuts import render
import re
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from pathlib import Path
from bgc_md.reports import defaults
from bgc_md.Model import Model
from bgc_md.component_schemes import  available_component_schemes
# Create your views here.
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

def model_overview(request,file_name):
    choices=available_component_schemes()

    dp=defaults()['paths']['data']
    ap=dp.joinpath('all_records')
    yaml_path=ap.joinpath(file_name)
    if yaml_path.exists():
         m=Model.from_path(yaml_path)
    else:
        # create an uninitialized instance
        m=object.__new__(Model)
        # set defaults
        m.yaml_component_type=choices[0]

    context={'yaml_file_name':file_name}
    return render(request,'yaml_creator/model_overview.html',context)


def detail(request,file_name):
    #dp=defaults()['paths']['data']
    #ap=dp.joinpath('all_records')
    #dp.joinpath("ComponentKeys.yaml")
    m=0  #placebo for model
    #template=loader.get_template('yaml_creator/detail.html')
    choices=available_component_schemes()
    context={'yaml_file_name':file_name,'choices':choices}
    #return render(request,'yaml_creator/detail.html',context)
    try:
        selected_choice=choices[int(request.POST['choice'])-1]
        print(selected_choice)
    except (KeyError):
        context= { 'yaml_file_name':file_name, 'choices'       :choices, 'error_message' :"You did not select a choice." }
        return render(request,'yaml_creator/detail.html',context)
    else:
        m+=1 #placebo for impact on model 

        #selected_choice=choices[request.POST['choice']-1]
        print("##############################")
        print(file_name)
        #print(request.POST['choice'])
        #print()
        print("##############################")
        template=loader.get_template('yaml_creator/soil_model_components.html')
        context={'yaml_file_name':file_name,'choices':choices}
        return HttpResponseRedirect(reverse('index'))

