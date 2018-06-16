from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme    import ComponentScheme   
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.Fluxes             import Fluxes            




def detail(request,file_name):
    #subclasses=FluxRepresentation.get_subclasses()
    #subclassNames=[f.__name__ for f in subclasses]
    try:
        modeldescriptor = ModelDescriptor.objects.get(pk=file_name)
    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
    template=loader.get_template('yaml_creator/detail.html')
    content= {'modeldescriptor': modeldescriptor}
    out=template.render(content,request)
    print('#########################')
    #print(request.POST)
    #key='component_scheme'
    #if key in request.POST.keys():
    #    print(subclassNames[int(request.POST['component_scheme'])-1])
    #    #md3=ModelDescriptor.objects.create(filename=file_name,pub_date=md.pub_date)
    #    cs= modeldescriptor.componentscheme
    #    f=Fluxes.objects.create(componentScheme=cs)
    #print('#########################')

    #if not(hasattr(modeldescriptor,"ComponentScheme")):
    #    cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
    #    cs.save()
    #    template=loader.get_template('yaml_creator/new_component_scheme.html')
    #    content.update({'subclasses': subclassNames})
    #    CreateCs=template.render(content,request)
    #    out+=CreateCs
    #    
    #
    ##T1= render(request, 'yaml_creator/detail.html',content)	
    return HttpResponse(out)
