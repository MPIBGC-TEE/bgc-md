from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme import ComponentScheme


@csrf_protect
def set_statevector(request,file_name):
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        try:
            cs=md.componentscheme
        except ComponentScheme.DoesNotExist as e:
            cs=ComponentScheme.objects.create(model_descriptor=md)
            cs.save()
        
        key='statevector'
        if not(key in request.POST.keys()):
        # if the form has not been used yet show it  
            template=loader.get_template('yaml_creator/set_statevector.html')
            content= {'modeldescriptor': md}
            out=template.render(content,request)
            return HttpResponse(out)
        else: 
            # if the form was used forward to the next side
            cs.statevector=request.POST[key]
            cs.save()
            target=reverse("set_statevariable_descriptions",kwargs={"file_name":file_name})
            return HttpResponseRedirect(target)

    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")
