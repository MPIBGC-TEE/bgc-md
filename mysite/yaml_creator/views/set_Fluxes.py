import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.Fluxes import Fluxes
from yaml_creator.models.InternalFlux import InternalFlux
from yaml_creator.models.InFlux import InFlux
from yaml_creator.models.OutFlux import OutFlux

def set_Fluxes(request,file_name):
    try:
        md = ModelDescriptor.objects.get(pk=file_name)
        try:
            spn=[var.name for var in md.componentscheme.statevector.statevariable_set.all()]
            pkeys=request.POST.keys()
            if len(pkeys)<1:
                fr=md.componentscheme.fluxes
                flux_tuples=[(f.source,f.target) for f in fr.internalflux_set.all()]
                flstr=json.dumps(flux_tuples)
                print('######################################## flstr 1:')
                print(type(flstr))
                print(flstr)
                print(spn)
                content= {
                    'modeldescriptor': md,
                    'pool_names':spn,
                    'flstr':flstr,
                    'fluxes':flux_tuples
                }
                template=loader.get_template('yaml_creator/edit_Fluxes.html')
                out=template.render(content,request)
                return HttpResponse(out)

                
            else:
                print(pkeys)
                s=request.POST['Source']
                t=request.POST['Target']
                print(s,t)
                #source=md.variable_set.get(name=s)
                #target=md.variable_set.get(name=t)
                #sf=InternalFlux(fluxes=fr, source=source, target=target)
                fr=md.componentscheme.fluxes
                sf=InternalFlux(fluxes=fr, source=s, target=t)
                sf.save()
                flux_tuples=[(f.source,f.target) for f in fr.internalflux_set.all()]
                flstr=json.dumps(flux_tuples)
                print('######################################## flstr 2:')
                print(type(flstr))
                print(flstr)
                template=loader.get_template('yaml_creator/edit_Fluxes.html')
                content= {
                    'modeldescriptor': md,
                    'pool_names':spn,
                    'flstr':flstr,
                    'fluxes':flux_tuples
                }
                out=template.render(content,request)
                return HttpResponse(out)
                #return HttpResponse('some fluxes have been set')
        except Fluxes.DoesNotExist as e:
            return HttpResponseRedirect(reverse("set_FluxRepresentation",kwargs={"file_name":file_name}))

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
