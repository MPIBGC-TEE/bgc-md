from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.models.ComponentScheme    import ComponentScheme   
from yaml_creator.models.FluxRepresentation import FluxRepresentation
from yaml_creator.models.Fluxes             import Fluxes            
from yaml_creator.forms import NameForm
from yaml_creator.forms import ModelDescriptorForm



def detail(request,file_name):
    #subclasses=FluxRepresentation.get_subclasses()
    #subclassNames=[f.__name__ for f in subclasses]
    template=loader.get_template('yaml_creator/detail.html')

    if request.method == 'POST':
        # this means the form had allready been displayed
        # and now somebody hit the submit button
        print("########################################")
        print("got POST request")
        form=ModelDescriptorForm(request.POST)
        print("form:")
        #print(form.__dict__)
        print(form.data)
        if form.is_valid():
            print("########################################")
            print('    form.cleaned_data')
            print(form.cleaned_data)
            #proces data in form.cleaned_data
            modeldescriptor = ModelDescriptor.objects.create(
                filename=file_name,
                pub_date=timezone.now()
            )
            modeldescriptor.save()
            # also created the (one to one) related Component scheme
            cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
            cs.save()

            return HttpResponseRedirect(reverse('data_base_index'))

        else:
            # reload with error messages
            # fixme 
            content= {
                'file_name'      : file_name,
                'form'           : form,
                 'error'         : 'something went wrong'
            }

    else:
        # poputlate the form with date from the data base or create a blank form
        #form=NameForm()
        try:
            md= ModelDescriptor.objects.get(pk=file_name)
            # populate the form with the stored data
            form=ModelDescriptorForm(initial={ 'pub_date': md.pub_date,'doi':md.doi})
            template=loader.get_template('yaml_creator/detail.html')
            
        except Exception as e :#ModelDescriptor.DoesNotExist:
            print("##########################################")
            print("The following exception occurred: "+str(e))
            print("##########################################")
            print('trying to create a new model')
            # create a new one
            form=ModelDescriptorForm(initial={ 'pub_date': timezone.now() })
            
        template=loader.get_template('yaml_creator/detail.html')
        content= {
            'file_name'      : file_name
            ,
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
