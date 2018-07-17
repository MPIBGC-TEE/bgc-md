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
            

            #VariableFormSet=inlineformset_factory(ModelDescriptor,Variable,fields=('description',),help_texts=['x1','x2','x3'])
            VariableFormSet=[StateVariableForm(prefix=var.name) for var in svs]
            #VariableFormSet=formset_factory(StateVariableForm,extra=0)
            #initial_svfs=[{'name': var.name} for var in svs]
            #vfs=VariableFormSet(initial=initial_svfs)

            template=loader.get_template('yaml_creator/StateVariable.html')
            
            #html_snippets=[
            #        template.render(
            #            {
            #                "name":var.name
            #                ,
            #                "form":StateVariableForm() 
            #            } 
            #        )
            #        for var in svs
            #]
            context["VariableFormSet"]=VariableFormSet

        except ComponentScheme.DoesNotExist as e:
            print(str(e))
            pass

        
    except ModelDescriptor.DoesNotExist as e:
        # prepare to show them once again
        initial_md['doi']='http://doi.org/'
        initial_md['pub_date']=timezone.now()

    context["ModelDescriptorForm"]=ModelDescriptorForm(initial=initial_md)
         
    return context
