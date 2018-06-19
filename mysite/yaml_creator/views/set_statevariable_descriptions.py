
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from sympy import sympify
from django.urls import reverse
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme
from yaml_creator.models.Variable import Variable

@csrf_protect
def set_statevariable_descriptions(request,file_name):

    try:
        md = ModelDescriptor.objects.get(pk=file_name)
        try:
            cs=md.componentscheme
            statevector=cs.statevector
            exp=sympify(statevector)
            var_list=[str(symb) for symb in exp.free_symbols]
            if len(request.POST.keys())<1: #show the page for the first time without the form submittet
                content= {
                    'modeldescriptor': md,
                    'var_list': var_list,
                }
                template=loader.get_template('yaml_creator/set_statevariable_descriptions.html')
                out=template.render(content,request)
                return HttpResponse(out)
            else:
                for var_name in var_list:
                    v=Variable.objects.create(name=var_name,model_descriptor=md)
                    v.save()

                return HttpResponseRedirect(reverse("set_FluxRepresentation",kwargs={"file_name":file_name}))

        except ComponentScheme.DoesNotExist as e:
            return HttpResponseRedirect(reverse("set_statevector",kwargs={"file_name":file_name}))

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
