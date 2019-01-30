import json
from django.forms.widgets import Widget,TextInput
from testinfrastructure.helpers import pe
class StateVectorInput(TextInput):
    template_name = 'yaml_creator/widgets/StateVectorInput.html'
    
    def format_value(self,var_names_list):
        if isinstance(var_names_list,list):
            res = ",".join(var_names_list)
        else:
            res=var_names_list    
        return res

class FluxesInput(Widget):
    #input_type = None  # Subclasses must define this.
    input_type = 'hidden'
    template_name = 'yaml_creator/widgets/FluxesInput.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
	        'type':self.input_type,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
        }

        return context
    def format_value(self,value):
        if isinstance(value,dict):
            res=json.dumps(value)
        elif isinstance(value,str):
            pe('value',locals())
            res=value
        return res

    class Media:
        js=[ "yaml_creator/js/FluxFields.js", ]
