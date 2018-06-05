#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from pathlib import Path
from bgc_md.reports import defaults
from bgc_md.Model import Model
# Create your views here.
def index(request):
    ap=defaults()['paths']['data'].joinpath('all_records')
    print(ap)
    template=loader.get_template('yaml_creator/index.html')
    yaml_file_names=[p.name for p in ap.iterdir()]
    context={'yaml_file_names':yaml_file_names}
    return HttpResponse(template.render(context,request))


def detail(request,file_name):
    #dp=defaults()['paths']['data']
    #ap=dp.joinpath('all_records')
    #m=Model.from_path(ap.joinpath())
    #dp.joinpath("ComponentKeys.yaml")
    m=0  #placebo for model
    template=loader.get_template('yaml_creator/detail.html')
    choices=["x=Bx+s","x=Ax+ub"] 
    try:
        selected_choice=choices[int(request.POST['choice'])-1]
        print(selected_choice)
    except (KeyError):
        return template.render(
            { 'yaml_file_name':file_name, 'choices'       :choices, 'error_message' :"You did not select a choice." }
            ,request
            )
    else:
        m+=1 #placebo for impact on model 

        #selected_choice=choices[request.POST['choice']-1]
        print("##############################")
        print(file_name)
        #print(request.POST['choice'])
        #print()
        print("##############################")
        template=loader.get_template('yaml_creator/SoilModelComponents.html')
        context={'yaml_file_name':file_name,'choices':choices}
        return HttpResponseRedirect(reverse('yaml_creator:index'))

