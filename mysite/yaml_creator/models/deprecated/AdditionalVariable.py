from django.db import models
from django.core.exceptions import ValidationError
from .ModelDescriptor import ModelDescriptor
from .Variable import Variable

     
class AdditionalVariable(Variable):
    model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    expression=models.CharField(max_length=200)
    
    def clean(self):
        #get all variables targeting the present ModelDescriptor
        md=self.model_descriptor
        add_vars=list(md.variable_set.all())
        state_vars=list(md.statevector.statevariable_set.all())
        all_vars=add_vars+state_vars
        self.mm_check(all_vars)
