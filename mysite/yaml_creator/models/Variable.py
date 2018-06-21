from django.db import models
from django.core.exceptions import ValidationError
from .ModelDescriptor import ModelDescriptor

#class VariableManager(models.Manager):
#    def create(self,*args,**kwargs):
#        var=super().create(*args,**kwargs)
#        #try: 
#        #    var.clean_post()
#        #except ValidationError as e:
#        #    var.delete()
#        #    raise(e)
#        #return var
     
class Variable(models.Model):
    name=models.CharField(max_length=200)

    model_descriptor=models.ForeignKey('ModelDescriptor',on_delete=models.CASCADE)
    reverse_execution_order_position=models.IntegerField(default=0)
    #objects=VariableManager()
    
    # opverlaod save to ensure that no duplicated 
    # variables are saved in the database
    # This automatically affects the manager
    # Variable.objects.create(...
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)

    # we provide a custom constructor to b
    # warned even before we try to save
    @classmethod
    def create(cls,*args,**kwargs):
        newVar=cls(*args,**kwargs)
        newVar.clean()
        #newWar.save()
        return(newVar)



    def clean(self):
        #get all variables targeting the present ModelDescriptor
        md=self.model_descriptor
        all_vars=list(md.variable_set.all())
        self.mm_check(all_vars)

    def mm_check(self,all_vars):
        print('##################3')
        print(all_vars)
        #remove the present (yet unsaved) variable 
        var_names=[var.name for var in all_vars]
        print(var_names)
        #now check if we allready have a variable of that name
        if self.name in var_names:
            raise ValidationError("The names of the variables have to be uniqe per model_descriptor. The variable: {} is already in the list: {}".format(self.name,var_names))

#    def clean_post(self):
#        md=self.model_descriptor
#        all_vars=list(md.variable_set.all())
#        all_vars.remove(self)
#        self.mm_check(all_vars)

