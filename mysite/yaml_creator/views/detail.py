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
from ..forms import NameForm
from ..forms import ModelDescriptorForm
#from .show_detail_page import show_detail_page
from .get_StateVariableForms import get_StateVariableForms
from .get_context import get_context 


def detail(request,file_name):
    # before we know which fields our form will have to have we have to find out which data are already present in the database
    extraFields=[]
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
                # to initialize the form for the statevariable descriptions makes only
                # sense if there are some
                svs=sv.statevariable_set.all()
                for var in svs:
                    extraFields.append('staveVariable_name_'+var.name)
                    extraFields.append('staveVariable_description'+var.name)

                extraFields.append("StateVector") 

                
            except StateVector.DoesNotExist as e:
                print('StateVector did not exist #####')
        except ComponentScheme.DoesNotExist as e:
            print('componentscheme did not exist #####')
    except ModelDescriptor.DoesNotExist as e:
        print('ModelDescriptor did not exist #####')
    
    print("###########################################")     
    print("############# extraFields ##############################")     
    print(extraFields)

        

    
    # if this is a POST request we need to process the form data
    if request.method== 'POST':
        print("############# called with request #############################")

        # create a ModelDescriptoForm instance and populate it with data from the request:
        rp=request.POST
        print(rp)
        
        form = ModelDescriptorForm(rp)

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
                print('################## ModelDescriptor existed already #####')
                # populate the existing md with the form data
                md.doi=cd['doi']
                md.pub_date=cd['pub_date']
                md.save()
                

                
            except ModelDescriptor.DoesNotExist as e:
                print('################## ModelDescriptor did not exist #####')
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
                print('################## componentschem existed already #####')

            except ComponentScheme.DoesNotExist as e:
                print('################## componentscheme did not exist #####')
                cs=ComponentScheme.objects.create(model_descriptor=md)
             
            try:
                sv=cs.statevector
                print('################## statevector existed already #####')
                sv.varliststring=cd["statevector"]
                # to initialize the form for the statevariable descriptions makes only
                # sense if there are some
                svs=sv.statevariable_set.all()
                initial_svfs=[{'name': var.name} for var in svs]
                nf=len(initial_svfs)
                StateVariableFormSet=get_StateVariableForms()
                erp=deepcopy(rp)
                #erp.update({'form-TOTAL_FORMS': nf,'form-INITIAL_FORMS': nf,'form-MAX_NUM_FORMS': '',})
                erp.update({'form-TOTAL_FORMS': nf,'form-INITIAL_FORMS': nf})
                variableforms=StateVariableFormSet(erp,initial=initial_svfs)
                if variableforms.is_valid():
                    for sf in variableforms:
                        sfcd=sf.cleaned_data
                        print("################ sfcd")
                        print(sfcd)
                        var=sv.statevariable_set.get(name=sfcd['name'])
                        var.description=sfcd['description']
                        var.save()
                    print("#############33 creates statevariables ############")

                
                print(variableforms.errors)
            except StateVector.DoesNotExist as e:
                sv=StateVector(componentscheme=cs,varliststring=cd["statevector"])
                print('################## StateVector did not exist #####')
            
            try:
                fr=cs.fluxRepresentation
                # Fluxrepresentation is an abstract class
                # we can only instatiate one of its subclasses
                # We find out which one by 
            except:
                pass

                #fr=Fluxrepresentation(componentscheme=cs,varliststring=cd["statevector"])

            sv.save()
            context=get_context(file_name)
            context['success']=request.POST
            # or redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
        else:
            # the form was not valid  an error occurred in 
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
        print("##################################################################")
        print("##################################################################")
        print("############# called without request #############################")
        #context=get_context(file_name)
        context={ 'file_name'      : file_name}
        # depending on the already available information in the draft with the given filename
        # different forms are created and initialized either with stored content or default values

        initial_md=dict()
        try:
            md= ModelDescriptor.objects.get(pk=file_name)
            print("############ ModelDescriptor found ##############################")
            # poputlate the form with data from the database
            initial_md['doi']=md.doi
            initial_md['pub_date']=md.pub_date
            try:
                cs=md.componentscheme
                print("############ componentscheme found ##############################")
                
                initial_md['statevector']=sv.varliststring
                try:
                    initial_md['fluxrepresentation']=cs.fluxrepresentation.__class__
                except Exception as e:
                    #initial_md['fluxrepresentation']= [c for c in FluxRepresentation.get_subclasses()[0]
                    initial_md['fluxrepresentation']= "Fluxes"
                

                StateVariableFormSet=get_StateVariableForms()
                initial_svfs=[{'name': var.name,'description':var.description} for var in svs]
                context["variableforms"]=StateVariableFormSet(initial=initial_svfs)
                #context["FluxRepresentationForm"]=FluxRepresentationForm()
                

            except ComponentScheme.DoesNotExist as e:
                print(str(e))




            
        except ModelDescriptor.DoesNotExist as e:
            # prepare to show them once again
            initial_md['doi']='http://doi.org/'
            initial_md['pub_date']=timezone.now()

        print("##########################################")
        print("initial_md")
        print(initial_md)
        print("##########################################")
        mdf=ModelDescriptorForm(initial=initial_md)
        print("mdf.fields")
        print(mdf.fields)
        context["ModelDescriptorForm"]=mdf 
         

    return render(request, 'yaml_creator/detail.html', context)
