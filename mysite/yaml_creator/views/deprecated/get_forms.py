from sympy import sympify

from django.utils import timezone
from django.forms import inlineformset_factory

from ..models.ModelDescriptor import ModelDescriptor
from ..models.ComponentScheme import ComponentScheme
from ..models.Variable import Variable
from ..forms import ModelDescriptorForm
from ..forms import StateVariableForm
from ..forms import AdditionalVariableForm

def get_forms(file_name):
    # depending on the already available information in the draft with the given filename
    # different forms are created and initialized either with stored content or default values
    FormDict=dict()

    initial_md=dict()
    try:
        md= ModelDescriptor.objects.get(pk=file_name)
        # populate the existing md with the form data
        initial_md['doi']=md.doi
        initial_md['pub_date']=md.pub_date
        try:
            cs=md.componentscheme
            initial_md['statevector']=cs.statevector
            

            #VariableFormSet=inlineformset_factory(ModelDescriptor,Variable,fields=('description',),help_texts=['x1','x2','x3'])
            VariableFormSet=[StateVariableForm(initial={'name':var.name}) for var in cs.statevariable_set.all()]
            print(VariableFormSet)
            FormDict["VariableFormSet"]=VariableFormSet

        except ComponentScheme.DoesNotExist as e:
            print(str(e))
            pass

        
    except ModelDescriptor.DoesNotExist as e:
        # prepare to show them once again
        initial_md['doi']='http://doi.org/'
        initial_md['pub_date']=timezone.now()

    form = ModelDescriptorForm(initial=initial_md)
    print(form)
    FormDict["ModelDescriptorForm"]=form
    return FormDict
