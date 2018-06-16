from django.http import HttpResponse, HttpResponseRedirect
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from django.utils import timezone
from django.template import loader
from django.urls import reverse

def create_new_ModelDescriptor(request):
    key='filename'
    if key in request.POST.keys():
        yaml_file_name=request.POST[key]
        modeldescriptor = ModelDescriptor.objects.create(
            filename=yaml_file_name,
            pub_date=timezone.now()
        )
        modeldescriptor.save()
        return HttpResponseRedirect(reverse("set_statevector",kwargs={"file_name":yaml_file_name}))
    #cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
    #cs.save()
    #template=loader.get_template('yaml_creator/new_component_scheme.html')
    #content= {'modeldescriptor': modeldescriptor}
    #out=template.render(content,request)
    ##return HttpResponse("Create the model here")
    #template=loader.get_template('yaml_creator/new_component_scheme.html')
    #content.update({'subclasses': subclassNames})
    #CreateCs=template.render(content,request)
    #out+=CreateCs
    #return HttpResponse(out)
    return HttpResponse(request)

