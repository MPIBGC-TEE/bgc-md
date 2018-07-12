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
    print("########################################")
    print ('in detail view')
    print("########################################")
    #subclasses=FluxRepresentation.get_subclasses()
    #subclassNames=[f.__name__ for f in subclasses]

    if request.method == 'POST':
        form=ModelDescriptorForm(request.POST)
        if form.is_valid():
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
            print("########################################")
            print('something went wrong')
            print("########################################")
            print(form.errors)
            print(form.data)
            print(form.changed_data)
            print(form.is_valid())
            print(form.has_changed())
            #for key,row in form.fields.items():
            #    print(row.)
            print("########################################")
            template=loader.get_template('yaml_creator/detail.html')
            content= {
                'file_name'      : file_name,
                'form'           : form,
                 'error'         : 'something went wrong'
            }

            out=template.render(content,request)
            return HttpResponse(out)
    else:
        # poputlate the form with date from the data base or create a blank form
        #form=NameForm()
        try:
            md= ModelDescriptor.objects.get(pk=file_name)
            # populate the form with the stored data
            form=ModelDescriptorForm(initial={ 'pub_date': md.pub_date,'doi':md.doi})
            template=loader.get_template('yaml_creator/detail.html')
            content= {
                'file_name'      : file_name
                ,
                'form'           : form
                ,
                'fieldset'           : form.fields
            }
            out=template.render(content,request)
            return HttpResponse(out)
            
            
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
                ,
                'fieldset'           : form.fields
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
