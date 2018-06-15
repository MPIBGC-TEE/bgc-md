from django.http import HttpResponse, HttpResponseRedirect
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from django.utils import timezone
from django.template import loader

def edit_ComponentScheme(request,modeldescriptor_filename):
    modeldescriptor = ModelDescriptor.objects.create(
        filename=modeldescriptor_filename,
        pub_date=timezone.now()
    )
    cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
    cs.save()
    template=loader.get_template('yaml_creator/new_component_scheme.html')
    content= {'modeldescriptor': modeldescriptor}
    out=template.render(content,request)
    #return HttpResponse("Create the model here")
    template=loader.get_template('yaml_creator/new_component_scheme.html')
    content.update({'subclasses': subclassNames})
    CreateCs=template.render(content,request)
    out+=CreateCs
    return HttpResponse(out)

