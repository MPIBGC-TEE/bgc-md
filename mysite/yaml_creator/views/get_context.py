from sympy import sympify

from django.utils import timezone
#from django.forms import inlineformset_factory
from django.forms import formset_factory

from django.template import loader
from ..models.ModelDescriptor import ModelDescriptor
from ..models.ComponentScheme import ComponentScheme
from ..models.Variable import Variable
from ..forms import ModelDescriptorForm
from ..forms import StateVariableForm
from ..forms import AdditionalVariableForm
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
            
            StateVariableFormSet=get_StateVariableForms()
            initial_svfs=[{'name': var.name,'description':var.description} for var in svs]
            context["variableforms"]=StateVariableFormSet(initial=initial_svfs)

        except ComponentScheme.DoesNotExist as e:
            print(str(e))




        
    except ModelDescriptor.DoesNotExist as e:
        # prepare to show them once again
        initial_md['doi']='http://doi.org/'
        initial_md['pub_date']=timezone.now()

    context["ModelDescriptorForm"]=ModelDescriptorForm(initial=initial_md)
         
    return context
