from copy import deepcopy

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect


#from ..models.ModelDescriptor import ModelDescriptor
#from ..models.StateVector import StateVector, StateVariable
#from ..models.ComponentScheme    import ComponentScheme   
#from ..models.FluxRepresentation import FluxRepresentation
#from ..models.Fluxes             import Fluxes            
#from ..models.Matrices import Matrices 
from ..forms import ModelDescriptorForm
from ..helpers import var_names_from_state_vector_string
from ..config import dataDir,defaultYamlFileName
import os
from pathlib import Path
from yaml import dump,load
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO 

def formDataFromYamlFile(file_name):
    ## before we know which fields our form needs we have to find out 
    ## what data are already present in the YamlFile
    p=Path(dataDir).joinpath(file_name)
    if p.exists():
        dp=p.joinpath(defaultYamlFileName)
        with dp.open("r") as f:
            new_rp=load(f.read())
    else:
        # otherwise let the form provide some sensible defaults
        new_rp={}
    return new_rp



def updateYamlFile(file_name,cd):
    print(os.getcwd())
    p=Path(dataDir).joinpath(file_name)
    if not p.exists():
        p.mkdir(parents=True)

    dp=p.joinpath(defaultYamlFileName)
    with dp.open("w") as f:
        f.write(dump(cd))

    
# a helper function that updated the model entry in thd database with the clean data
def detail(request,file_name):
    context={
        'file_name'      : file_name
    }
    
    # if this is a POST request we need to process the form data
    if request.method== 'POST':
        print("############# called with request #############################")

        # create a ModelDescriptoForm instance and populate it with data from the request:
        rp=request.POST
        # Note that this view will be called several times before a ModelDescriptor     
        # is completed (or even saved for the first time).
        # 0.)   Before we receive the first POST (and thus BEFORE 
        #       this part of the code is executed for the first time) 
        #       the initial instance of 
        #       ModelDescriptorForm had had only some static fields filled
        #       with default values. An html form had been created and rendered.
        #       The user changed some values in the fields and 
        #       hit the submit button, triggering a POST request.
        #       
        # 1.)   When we receive this POST request, this  part of the code is executed 
        #       for the first time. Several things have to happen.
        #       a.) 
        #           The received data have to be validated (and stored):
        #           To this end a new form instance is created from the data 
        #           in the POST using the same static fields 
        #           as the initial instance but with new values from the request
        #           and then the is_valid method is called on the instance.
        #
        #           old_form=old_form(rp)
        #           if old_form.is_valid()):
        #               persist data                   
        #           else
        #               repeat step 1
        #       b.) 
        #           Before the form instanciated to be  DISPLAYED 
        #           the next time it has to be extended by new fields, 
        #           filled with default values 
        #           (For instance state variable fields with names depending on the 
        #           statevector received in the first POST).
        #
        #           new_form=new_form(rp,newFieldsWithDefaults)
        #
        # 2.)  When we receive the second POST similar things have to happen:
        #       a.)
        #           Create a form instance that contains the same fields
        #           the new_form instance last displayed (under 1 b) had.
        #
        #           if old_form.is_valid()):
        #               persist data                   
        #           else
        #               repeat step 2
        #       b.) 
        #           Create a new form instance to be DISPLAYED with new fields 
        #           added.
        # 
        #           new_form=new_form(rp,newFieldsWithDefaults)
        # .
        # .
        # .
        # N.)  When we receive the N-th POST we have to:
        #       a.)
        #           Create a form instance that contains the same fields
        #           the instance last displayed (under N-1 b) had.
        #
        #           old_form=old_form(rp) 
        #           if old_form.is_valid()):
        #               persist data                   
        #           else
        #               repeat step N
        #       b.) 
        #           Create a new form instance to be DISPLAYED with new fields 
        #           added.
        # 
        #           new_form=new_form(rp,newFieldsWithDefaults)
        #       
        # Notice that in steps from 2 to N a) we must choose the fields of the form depending
        # on the POST data rp. 
        # We cuold do that by building the a form class cls on demand by a 
        # class factory function e.g. FormClassByData and then using the tailormade
        # class cls to create an instance with the data:
        #
        # old_cls=FormClassByData(rp.keys())
        # old_form=old_cls(rp)
        # new_cls=FormClassByData(rp.keys()+MewFieldsWithDefaults.keys())
        # new_form=new_cls(rp+NewFieldsWithDefaults)

        # But since we only need ONE instance we can move the 
        # adaptation in the
        # __init__ method of a class that stays constant but can produce instances
        # with different fields 


        old_form = ModelDescriptorForm(rp)

        # check whether it's valid:
        if old_form.is_valid():
            # process the data in old_form.cleaned_data as required
            # ...
            cd = old_form.cleaned_data
            # update the database
            # updateModelDescriptor(file_name,cd)
            updateYamlFile(file_name,cd)
            
            # extend the form by new fields required in the next step
            new_form,new_rp=old_form.extended_instance()
            
            imgdata=StringIO()
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot([1,2,3])
            fig.savefig(imgdata,format='svg')

            context['plot']=imgdata.getvalue()
            context['ModelDescriptorForm'] =new_form
            context['success']=request.POST
            context['inspect']={"new_rp":new_rp}
        

        else:
            # the form was not valid  an error occurred 
            for name,field in old_form.fields.items():
                print(name)
                print(field)


            context={
                'file_name'     :file_name
                ,
                'form'          :old_form
                ,
                'doi_dict':old_form.fields['doi'].__dict__
                ,
                'error':old_form.errors
            }


    
    else:
        # if we received a GET (or any other method but POST) we'll create a form 
        # filled from the yaml file(if we have one) or a blank form (with some defaults)
        print("############# called without request #############################")
        context={ 'file_name'      : file_name}
        #new_rp=formDataFromDatabase(file_name)
        new_rp=formDataFromYamlFile(file_name)

        #new_form = ModelDescriptorForm()
        new_form = ModelDescriptorForm(initial=new_rp)
        context['ModelDescriptorForm'] =new_form

         

    return render(request, 'yaml_creator/detail.html', context)
