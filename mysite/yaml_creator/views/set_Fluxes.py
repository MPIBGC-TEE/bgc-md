
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.SingleFlux import SingleFlux

def set_Fluxes(request,file_name):
    try:
        md = ModelDescriptor.objects.get(pk=file_name)
        try:
            fr=md.componentscheme.fluxrepresentation
            spn=[var.name for var in md.variable_set.all()]
            tpn=spn.copy()
            pkeys=request.POST.keys()
            if len(pkeys)<1:
                template=loader.get_template('yaml_creator/set_Flux.html')
                content= {
                    'modeldescriptor': md,
                    'source_pool_names':spn,
                    'target_pool_names':tpn
                }
                out=template.render(content,request)
                return HttpResponse(out)

                
            else:
                print('######################################## source target:')
                print(pkeys)
                s=request.POST['Source']
                t=request.POST['Target']
                print(s,t)
                source=md.variable_set.get(name=s)
                target=md.variable_set.get(name=t)
                sf=SingleFlux( source=source, target=target)
                sf.save()
                return HttpResponse('some fluxes have been set')
        except FluxRepresentation.DoesNotExist as e:
            return HttpResponseRedirect(reverse("set_FluxRepresentation",kwargs={"file_name":file_name}))

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
