
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from yaml_creator.models.ModelDescriptor import ModelDescriptor

@csrf_protect
def set_statevariable_descriptions(request,file_name):
    try:
        modeldescriptor = ModelDescriptor.objects.get(pk=file_name)
    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
    
    key='statevector'
    if key in request.POST.keys():
        statevector=request.POST[key]
        modeldescriptor_statevector=statevector,
        template=loader.get_template('yaml_creator/set_statevariable_descriptions.html')
        content= {'modeldescriptor': modeldescriptor}
        out=template.render(content,request)
        return HttpResponse(out)
