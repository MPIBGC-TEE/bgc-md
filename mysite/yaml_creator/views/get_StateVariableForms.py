
from django.forms import formset_factory
from ..forms import StateVariableForm
def get_StateVariableForms():
    StateVariableFormSet=formset_factory(StateVariableForm,extra=0)
    return StateVariableFormSet
        #variableforms=[StateVariableForm(prefix=var.name,initial={"name":var.name,"description":var.description}) for var in svs]
        

        #variableforms=inlineformset_factory(ModelDescriptor,Variable,fields=('description',),help_texts=['x1','x2','x3'])

        #template=loader.get_template('yaml_creator/StateVariable.html')
        
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

