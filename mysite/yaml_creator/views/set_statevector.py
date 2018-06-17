from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme


@csrf_protect
def set_statevector(request,file_name):
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        try:
            cs=md.componentscheme
        except ComponentScheme.DoesNotExist as e:
            print('#######################33')
            print(type(e))
            print('#######################33')
            cs=ComponentScheme.objects.create(model_descriptor=md)
            cs.save()
        
        # if the form was used forward to the next side
        key='statevector'
        if key in request.POST.keys():
            statevector=request.POST[key]
            cs_statevector=statevector,
            cs.save()
            exp=sympify(statevector)
            var_list=[str(symb) for symb in exp.free_symbols]
            content= {
                'modeldescriptor': md,
                'var_list': var_list,
            }

            template=loader.get_template('yaml_creator/set_statevariable_descriptions.html')
            
            out=template.render(content,request)
            return HttpResponse(out)
        else:
        # if the form has not been used yet show it  
            template=loader.get_template('yaml_creator/set_statevector.html')
            content= {'modeldescriptor': md}
            out=template.render(content,request)
            return HttpResponse(out)

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
