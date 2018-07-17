from string import Template
from sympy import sympify
from .ComponentScheme import ComponentScheme
from .Variable import Variable
from django.db import models
from django.core.exceptions import ValidationError

class StateVariable(Variable):
    statevector=models.ForeignKey('StateVector',on_delete=models.CASCADE)

class StateVector(models.Model):
    componentscheme=models.OneToOneField('ComponentScheme',on_delete=models.CASCADE)
    varliststring=models.CharField(max_length=400)
    #fluxrep=models.OneToOneField(FluxRepresentation,on_delete=models.CASCADE,primary_key=True)

    
    # opverlaod save to ensure that no duplicated 
    # inconsistent statevectors are saved in the database
    # This automatically affects the manager
    # StateVector.objects.create(...

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)

        # now update the missing statevariables if necessary
        sss='Matrix([' + self.varliststring + '])'
        print('1#######################')
        exp=sympify(sss)
        print(exp)
        # determine the statevarables that we need
        needed_vars=set([str(symb) for symb in exp.free_symbols])
        print('needed_vars')
        print(needed_vars)

        saved_vars=set([var.name for  var in  self.statevariable_set.all()])
        print('saved_vars')
        print(saved_vars)
        missing_vars=needed_vars.difference(saved_vars)

        for var_name in missing_vars:
            v=StateVariable(name=var_name,statevector=self)
            v.save()

        self.clean()

    def clean(self):
        #get all variables targeting the present ModelDescriptor
        var_names_list=self.varliststring.split(',')
        var_names_set=set(var_names_list)
        if len(var_names_list)!=len(var_names_set):
            raise ValidationError(
                Template("The vartiable names in the  string representation of the statevector were not unique").subs(v=varliststring)
                )
        

        state_var_names=set([ var.name for var in self.statevariable_set.all()])
        print('##########################################')
        print("state_var_names")
        print(state_var_names)
        print("var_name_set")
        print(var_names_set)
        print('##########################################')
        if state_var_names!=var_names_set:
            raise ValidationError(
                Template("The variable names in the statevector and the set of state variables are different: ${s} ${svn}").subs(s=var_names_set, svn=state_var_names)
                )

                    
