from sympy import sympify

from django.utils import timezone
#from django.forms import inlineformset_factory
from django.forms import formset_factory

from django.template import loader
from ..models.ModelDescriptor import ModelDescriptor
from ..models.ComponentScheme import ComponentScheme
from ..models.FluxRepresentation import FluxRepresentation
from ..forms import ModelDescriptorForm , StateVariableForm , AdditionalVariableForm , FluxRepresentationForm
from .get_StateVariableForms import get_StateVariableForms

def get_context(file_name):
    context={ 'file_name'      : file_name}
    # depending on the already available information in the draft with the given filename
    # different forms are created and initialized either with stored content or default values

    initial_md=dict()
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        # populate the existing md with the form data
        initial_md['doi']=md.doi
        initial_md['pub_date']=md.pub_date
        try:
            cs=md.componentscheme
            
            sv=cs.statevector
            svs=sv.statevariable_set.all()
            initial_md['statevector']=sv.varliststring
            try:
                initial_md['fluxrepresentation']=cs.fluxrepresentation.__class__
            except Exception as e:
                print("##########################################")
                print(e)
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

    mdf=ModelDescriptorForm(initial=initial_md)
    print("##########################################")
    print("initial_md")
    print(initial_md)
    print("mdf.fields")
    print(mdf.fields)
    context["ModelDescriptorForm"]=mdf 
         
    return context
