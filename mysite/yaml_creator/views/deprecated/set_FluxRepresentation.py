from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.Fluxes import Fluxes
from yaml_creator.models.Matrices import Matrices


@csrf_protect
def set_FluxRepresentation(request,file_name):
    try:
        md = ModelDescriptor.objects.get(pk=file_name)
        try:
            cs=md.componentscheme
            sv=cs.statevector
            # fixme check if the variable are set and redirect to set_state_variable_descriptions if not
            subClasses=FluxRepresentation.get_subclasses()
            subClassNames=[f.__name__ for f in subClasses]
            key='FluxRepresentation'
            if not(key in request.POST.keys()):
                template=loader.get_template('yaml_creator/set_FluxRepresentation.html')
                content= {
                    'modeldescriptor': md,
                    'subClassNames': subClassNames
                }
                out=template.render(content,request)
                return HttpResponse(out)
            else:
                print('########################################333')
                className=request.POST[key]
                target=reverse("set_"+className,kwargs={"file_name":file_name})
                print('########################################333')
                print(target)
                print('########################################333')
                cls=globals()[className]
                print('########################################333')
                print(cls)
                try:
                    fr=getattr(cs,className.lower())
                    fr.delete()
                except ObjectDoesNotExist as e:
                    print(e)
                    fr=cls(componentscheme=cs)
                    fr.save()

                return HttpResponseRedirect(target)
        except ComponentScheme.DoesNotExist as e:
            return HttpResponseRedirect(reverse("set_statevector",kwargs={"file_name":file_name}))

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
