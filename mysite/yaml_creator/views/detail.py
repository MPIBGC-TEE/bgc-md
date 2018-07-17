from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect


from ..models.ModelDescriptor import ModelDescriptor
from ..models.StateVector import StateVector
from ..models.ComponentScheme    import ComponentScheme   
from ..models.FluxRepresentation import FluxRepresentation
from ..models.Fluxes             import Fluxes            
from ..forms import NameForm
from ..forms import ModelDescriptorForm
#from .show_detail_page import show_detail_page
from .get_context import get_context 

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
                

                
            except ModelDescriptor.DoesNotExist as e:
                print("##########################################")
                print("The following exception occurred: "+str(e))
                print("##########################################")
                print('trying to create a new model')
                # create a new one
                md = ModelDescriptor.objects.create(
                    filename=file_name,
                    doi=cd['doi'],
                    pub_date=cd['pub_date']
                )
                md.save()
                # also created the (one to one) related Component scheme
            
            try:
               # we find out if the request containe
                cs=md.componentscheme

            except ComponentScheme.DoesNotExist as e:
                cs=ComponentScheme.objects.create(model_descriptor=md)
             
            try:
                sv=cs.statevector
                sv.varliststring=cd["statevector"]
            except StateVector.DoesNotExist as e:
                sv=StateVector(componentscheme=cs,varliststring=cd["statevector"])

            sv.save()
            print("##########################################")
            print('sv.statevariable_set.all()')
            print(sv.statevariable_set.all())
            print("##########################################")
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
        context=get_context(file_name)

    return render(request, 'yaml_creator/detail.html', context)
