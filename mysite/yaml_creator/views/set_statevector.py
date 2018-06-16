
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from yaml_creator.models.ModelDescriptor import ModelDescriptor

@csrf_protect
def set_statevector(request,file_name):
    try:
        modeldescriptor = ModelDescriptor.objects.get(pk=file_name)
    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
    template=loader.get_template('yaml_creator/set_statevector.html')
    content= {'modeldescriptor': modeldescriptor}
    out=template.render(content,request)
    return HttpResponse(out)
