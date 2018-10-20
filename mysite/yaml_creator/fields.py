from django.forms import Field, URLField, DateField,CharField
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from .widgets import FluxesInput, StateVectorInput
from testinfrastructure.helpers import pe,pp
import json
import re
from string import Template
from copy import copy
from sympy import sympify,SympifyError,Symbol


class DOIField(URLField):
    pass
    # we could implement a special validation method here

class StateVectorField(CharField):
    widget = StateVectorInput
    default_error_messages={
            'not unique':"The variable names in the  string representation of the statevector were not unique. The following variables appeared more than once:",
            'wrong format':"We expect the variable names separated by commas. (without any brackets,or quotation marks)  ",
            'sympify':"Sympy could not parse the function_expressions."
            }

    def validate(self,varliststring):
        try:
            sym=sympify(varliststring)
            if isinstance(sym,tuple):
                symtup=sym
            elif isinstance(sym,Symbol):    
                symtup=(sym,)
            else:
                raise ValidationError(
                    self.default_error_messages['wrong format'],
                    code='wrong format')
                
        
            var_names_list=[n for n in map(str,symtup)]
        except SympifyError as e:
            var_names_list=[]
            raise ValidationError(
                Template("${message} ${v}").substitute(message=self.default_error_messages['sympify'],v=str(e)
            ),code='sympify')
        super().validate(varliststring)
        
        var_names_set=set(var_names_list)
        nue=copy(var_names_list)
        for var in var_names_set:
            nue.pop(nue.index(var))
        if len(var_names_list)!=len(var_names_set):
            raise ValidationError(
                    Template("${message} ${v}").substitute(message=self.default_error_messages['not unique'],v=str(nue)),
                    code='not unique'
            )


class PUB_DATEField(DateField):
    widget=AdminDateWidget
    # we could implement a special validation method here

class FluxesField(Field):
    widget = FluxesInput
    default_error_messages = {
        'invalid': ('This is a placeholder message It has to be constructed given the acutual fluxes.'),
    }
    re_decimal = re.compile(r'\.0*\s*$')

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

    def to_python(self, value):
        pp('value',locals())
        """
        """
        # the inner application yields a string
        fluxesDict=json.loads(value) 
        pp('fluxesDict',locals())
        return fluxesDict

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        if isinstance(widget, FluxesInput):
            attrs['test'] = 42
        return attrs
