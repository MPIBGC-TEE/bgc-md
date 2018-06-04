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

def detail(request,question_id):
    return HttpResponse("You are looking at question %s." % question_id)

def results(request,question_id):
    return HttpResponse("You are looking at the results of question %s." % question_id)

def change(request,file_name):
    #m=Model.from_
    template=loader.get_template('yaml_creator/change.html')
    ap=defaults()['paths']['data'].joinpath('all_records')
    choices=["x=Bx+s","x=Ax+ub"] 
    #selected_choice=choices[request.POST['choice']-1]
    print("##############################")
    print(file_name)
    print(choices[int(request.POST['choice'])-1])
    print("##############################")
    context={'yaml_file_name':file_name,'choices':choices}
    return HttpResponse(template.render(context,request))

