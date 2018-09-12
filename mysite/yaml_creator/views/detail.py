from copy import deepcopy

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect


from ..models.ModelDescriptor import ModelDescriptor
from ..models.StateVector import StateVector, StateVariable
from ..models.ComponentScheme    import ComponentScheme   
from ..models.FluxRepresentation import FluxRepresentation
from ..models.Fluxes             import Fluxes            
from ..forms import ModelDescriptorForm
#from ..forms import NameForm
#from .show_detail_page import show_detail_page
#from .get_StateVariableForms import get_StateVariableForms
#from .get_context import get_context 

def formDataFromDatabase(file_name):
    ## before we know which fields our form needs we have to find out 
    ## what data are already present in the database
    new_rp={}
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        print('ModelDescriptor existed already #####')
        # populate the existing md with the form data
        try:
           # we find out if the model_descriptor contains a componentscheme
            cs=md.componentscheme
            print('componentschem existed already #####')
            try:
                sv=cs.statevector
                print('statevector existed already #####')
                new_rp.update({"StateVector":sv})
                # to initialize the form for the statevariable descriptions makes only
                # sense if there are some
                svs=sv.statevariable_set.all()

                for var in svs:
                    name_key=ModelDescriptorForm.stateVarNameKey+var.name
                    desc_key=ModelDescriptorForm.stateVarDescKey+var.name
                    new_rp.update( {
                        name_key:var.name ,
                        desc_key:var.description
                        })


                try:
                    new_rp['fluxrepresentation']=cs.fluxrepresentation.__class__
                except Exception as e:
                    #new_rp['fluxrepresentation']= [c for c in FluxRepresentation.get_subclasses()[0]
                    new_rp['fluxrepresentation']= "Fluxes"
                
            except StateVector.DoesNotExist as e:
                print('StateVector did not exist #####')
        except ComponentScheme.DoesNotExist as e:
            print('componentscheme did not exist #####')
    except ModelDescriptor.DoesNotExist as e:
        print('ModelDescriptor did not exist #####')
    
    print("###########################################")     
    print("############# new_rp ##############################")     
    print(new_rp)
    return new_rp

# a helper function that updated the model entry with the clean data
def updateModelDescriptor(file_name,cd):
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        #print('################## ModelDescriptor existed already #####')
        # populate the existing md with the form data
        md.doi=cd['doi']
        md.pub_date=cd['pub_date']
        md.save()
        
    
        
    except ModelDescriptor.DoesNotExist as e:
        #print('################## ModelDescriptor did not exist #####')
        # create a new one
        md = ModelDescriptor.objects.create(
            filename=file_name,
            doi=cd['doi'],
            pub_date=cd['pub_date']
        )
        md.save()
        # also created the (one to one) related Component scheme
    
    try:
       # we find out if the model_descriptor contains a componentscheme
        cs=md.componentscheme
        #print('################## componentschem existed already #####')
    
    except ComponentScheme.DoesNotExist as e:
        #print('################## componentscheme did not exist #####')
        cs=ComponentScheme.objects.create(model_descriptor=md)
     
    try:
        sv=cs.statevector
        #print('################## statevector existed already #####')
        sv.varliststring=cd["statevector"]
       
       #svs=sv.statevariable_set.all()
        #initial_svfs=[{'name': var.name} for var in svs]
        #nf=len(initial_svfs)
        #StateVariableFormSet=get_StateVariableForms()
        #erp=deepcopy(rp)
        ##erp.update({'form-TOTAL_FORMS': nf,'form-INITIAL_FORMS': nf,'form-MAX_NUM_FORMS': '',})
        #erp.update({'form-TOTAL_FORMS': nf,'form-INITIAL_FORMS': nf})
        #variableforms=StateVariableFormSet(erp,initial=initial_svfs)
        #if variableforms.is_valid():
        #    for sf in variableforms:
        #        sfcd=sf.cleaned_data
        #        var=sv.statevariable_set.get(name=sfcd['name'])
        #        var.description=sfcd['description']
        #        var.save()
    
        
    except StateVector.DoesNotExist as e:
        #svs=sv.statevariable_set.all()
        sv=StateVector(componentscheme=cs,varliststring=cd["statevector"])
    
    sv.save()
    
    try:
        fr=cs.fluxRepresentation
        # Fluxrepresentation is an abstract class
        # we can only instatiate one of its subclasses
        # We find out which one by 
    except:
        pass
    
        #fr=Fluxrepresentation(componentscheme=cs,varliststring=cd["statevector"])
    

def detail(request,file_name):
    context={
        'file_name'      : file_name
    }
    
    # if this is a POST request we need to process the form data
    if request.method== 'POST':
        print("############# called with request #############################")

        # create a ModelDescriptoForm instance and populate it with data from the request:
        rp=request.POST
        print(rp)
        # Note that this view will be called several times before a model     
        # is completed.
        # 0.)   Before we receive the first POST (and this part of the code is
        #       executed for the first time) the initial instance of 
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
        #           if old_form.is_valid():
        #               incorporate data into the database
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
        #           old_form=old_form(rp) 
        #           if old_form.is_valid():
        #               incorporate data into the database
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
        #           if old_form.is_valid():
        #               incorporate data into the database
        #       b.) 
        #           Create a new form instance to be DISPLAYED with new fields 
        #           added.
        # 
        #           new_form=new_form(rp,newFieldsWithDefaults)
        #       
        # Notice that in steps 2-N a) we must choose the fields of the form depending
        # on the POST data rp. 
        # We cuold do that by building the a form class cls on demand by a 
        # class factory function e.g. FormClassByData and then using the tailormade
        # class cls to create an instance with the data:
        #
        # old_cls=FormClassByData(rp.keys())
        # old_form=old_cls(rp)
        # new_cls=FormClassByData(rp.keys()+MewFieldsWithDefaults.keys())
        # new_form=new_cls(rp+NewFieldsWithDefaults)

        # or we could tailormake the instance by moving the adaptation in the
        # __init__ method of a class that stays constant but can produce instances
        # with different fields 


        old_form = ModelDescriptorForm(rp)

        # check whether it's valid:
        if old_form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            cd = old_form.cleaned_data
            # update the database
            updateModelDescriptor(file_name,cd)
            
            # extend the form by new fields required in the next step
            #new_rp=deepcopy(rp)
            new_rp=formDataFromDatabase(file_name)

            new_form = ModelDescriptorForm(initial=new_rp)
            context['ModelDescriptorForm'] =new_form
            context['success']=request.POST
        
    
            #context=get_context(file_name)
            # or redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            
            
            #before we send the form to the template we extended with the fields 
            # that have to be there for the next step


        else:
            # the form was not valid  an error occurred 
            for name,field in form.fields.items():
                print(name)
                print(field)

            context={
                'file_name'      : file_name
                ,
                'form':old_form
                ,
                'doi_dict':form.fields['doi'].__dict__
                ,
                'error':form.errors
            }


    
    # if a GET (or any other method) we'll create a form 
    # filled from the database or a blank form
    else:
        print("##################################################################")
        print("##################################################################")
        print("############# called without request #############################")
        #context=get_context(file_name)
        context={ 'file_name'      : file_name}
        new_rp=formDataFromDatabase(file_name)

        #new_form = ModelDescriptorForm()
        new_form = ModelDescriptorForm(initial=new_rp)
        context['ModelDescriptorForm'] =new_form
        # depending on the already available information in the draft with the given filename
        # different forms are created and initialized either with stored content or default values

        #initial_md=dict()
        #try:
        #    md= ModelDescriptor.objects.get(pk=file_name)
        #    print("############ ModelDescriptor found ##############################")
        #    # poputlate the form with data from the database
        #    initial_md['doi']=md.doi
        #    initial_md['pub_date']=md.pub_date
        #    try:
        #        cs=md.componentscheme
        #        print("############ componentscheme found ##############################")
        #        
        #        initial_md['statevector']=sv.varliststring
        #        try:
        #            initial_md['fluxrepresentation']=cs.fluxrepresentation.__class__
        #        except Exception as e:
        #            #initial_md['fluxrepresentation']= [c for c in FluxRepresentation.get_subclasses()[0]
        #            initial_md['fluxrepresentation']= "Fluxes"
        #        

        #        StateVariableFormSet=get_StateVariableForms()
        #        initial_svfs=[{'name': var.name,'description':var.description} for var in svs]
        #        context["variableforms"]=StateVariableFormSet(initial=initial_svfs)
        #        #context["FluxRepresentationForm"]=FluxRepresentationForm()
        #        

        #    except ComponentScheme.DoesNotExist as e:
        #        print(str(e))




        #    
        #except ModelDescriptor.DoesNotExist as e:
        #    # prepare to show them once again
        #    initial_md['doi']='http://doi.org/'
        #    initial_md['pub_date']=timezone.now()

        #print("##########################################")
        #print("initial_md")
        #print(initial_md)
        #print("##########################################")
        #mdf=ModelDescriptorForm(initial=initial_md)
        #print("mdf.fields")
        #print(mdf.fields)
        #context["ModelDescriptorForm"]=mdf 
         

    return render(request, 'yaml_creator/detail.html', context)
