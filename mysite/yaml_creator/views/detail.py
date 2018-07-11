from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme    import ComponentScheme   
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.Fluxes             import Fluxes            
from yaml_creator.forms import NameForm
from yaml_creator.forms import ModelDescriptorForm



def detail(request,file_name):
    #subclasses=FluxRepresentation.get_subclasses()
    #subclassNames=[f.__name__ for f in subclasses]
    try:
        modeldescriptor = ModelDescriptor.objects.get(pk=file_name)
    except ModelDescriptor.DoesNotExist:
        raise Http404("ModelDescriptor does not exist")

    if request.method == 'POST':
        form=ModelDescriptorForm()
        if form.is_valid():
            #proces data in form.cleaned_data
            modeldescriptor = ModelDescriptor.objects.create(
                filename=yaml_file_name,
                pub_date=timezone.now()
            )
            modeldescriptor.save()
            # also created the (one to one) related Component scheme
            cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
            cs.save()

            return HttpResponseRedirect('/data_base_index/')
        else:
            # reload with error messages
            # fixme 
            template=loader.get_template('yaml_creator/detail.html')
            content= {
                'modeldescriptor': modeldescriptor,
                'form'           : form,
		'error'		 : 'something went wrong'
            }

            out=template.render(content,request)
            return HttpResponse(out)
    else:
        # poputlate the form with date from the data base or create a blank form
        #form=NameForm()
        try:
            md= ModelDescriptor.objects.get(pk=file_name)
            # populate the form with the stored data
            form=ModelDescriptorForm(initial={ 'pub_date': timezone.now() })
            template=loader.get_template('yaml_creator/detail.html')
            content= {
                'modeldescriptor': modeldescriptor,
                'form'           : form
            }
            out=template.render(content,request)
            return HttpResponse(out)
            
            
        except ModelDescriptor.DoesNotExist:
            # create a new one
            form=ModelDescriptorForm(initial={ 'pub_date': timezone.today() })
            template=loader.get_template('yaml_creator/detail.html')
            content= {
                'modeldescriptor': modeldescriptor,
                'form'           : form
            }
            out=template.render(content,request)
            return HttpResponse(out)
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
