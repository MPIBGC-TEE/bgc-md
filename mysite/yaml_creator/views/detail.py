from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.forms import inlineformset_factory

from sympy import sympify

from ..models.ModelDescriptor import ModelDescriptor
from ..models.ComponentScheme    import ComponentScheme   
from ..models.FluxRepresentation import FluxRepresentation
from ..models.Fluxes             import Fluxes            
from ..forms import NameForm
from ..forms import ModelDescriptorForm

def detail(request,file_name):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        #form = NameForm(request.POST)
        form = ModelDescriptorForm(request.POST)
        context={
            'file_name'      : file_name
            ,
            'form':form
        }
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            cd = form.cleaned_data
            try:
                md= ModelDescriptor.objects.get(pk=file_name)
                # populate the existing md with the form data
                md.doi=cd['doi']
                md.pub_date=cd['pub_date']
                md.save()
                try:
                    # we find out if the request containe
                    cs=md.componentscheme

                except ComponentScheme.DoesNotExist as e:
                    cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
                
                    #statevector=cs.statevector
                    #exp=sympify(statevector)
                    #var_list=[str(symb) for symb in exp.free_symbols]
                    ##determine the statevarables that have not been saved yet
                    ## the names of saved state varables  are
                    #svn=set([var.name for  var in  md.variable_set.all()])
                    ## the still missing ones
                    #msvn=var_list-snv
                    ## create them
                    #for var_name in msvn:
                    #    v=Variable.objects.create(name=var_name,model_descriptor=md)
                    #    v.save()
                    #VariableFormSet=inlineformset_factory(ModelDescriptor,Variable,fields=desc)

                
            except ModelDescriptor.DoesNotExist as e:
                print("##########################################")
                print("The following exception occurred: "+str(e))
                print("##########################################")
                print('trying to create a new model')
                # create a new one
                modeldescriptor = ModelDescriptor.objects.create(
                    filename=file_name,
                    doi=cd['doi'],
                    pub_date=cd['pub_date']
                )
                modeldescriptor.save()
                # also created the (one to one) related Component scheme
                cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
            finally :
                cs.statevector=cd["statevector"]
                cs.save()
                # prepare to show them once again
                context={'success':cd}
                # or redirect to a new URL:
                #return HttpResponseRedirect('/thanks/')
        else:
            # the form was not valid  an error occurred in 
            print('##########################################')
            for name,field in form.fields.items():
                print(name)
                print(field)

            context={
                'file_name'      : file_name
                ,
                'form':form
                ,
                'doi_dict':form.fields['doi'].__dict__
                ,
                'error':form.errors
            }


    # if a GET (or any other method) we'll create a form 
    # filled from the database or a blank form
    else:
        try:
            md= ModelDescriptor.objects.get(pk=file_name)
            # populate the form with the stored data
            initial={
                'doi':md.doi
                 ,
                'pub_date': md.pub_date
            }
            try:
                # we find out if the request containe
                cs=md.componentscheme
                initial['statevector']=cs.statevector

            except ComponentScheme.DoesNotExist as e:
                cs=ComponentScheme.objects.create(model_descriptor=modeldescriptor)
            
        except ModelDescriptor.DoesNotExist as e:
            print("##########################################")
            print("The following exception occurred: "+str(e))
            print("##########################################")
            print('trying to create a new model')
            # create a new one
            initial={
                'your_name':'http://google.com'
                 ,
                'pub_date': timezone.now()
            }
            #form = NameForm(initial=initial)

        finally:    
            form = ModelDescriptorForm(initial=initial)
            context={
                'file_name'      : file_name
                ,
                'form':form
            }

    return render(request, 'yaml_creator/detail.html', context)
