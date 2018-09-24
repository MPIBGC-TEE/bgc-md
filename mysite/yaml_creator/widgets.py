import json
from django.forms.widgets import Widget
class FluxesInput(Widget):
    #input_type = None  # Subclasses must define this.
    #template_name = 'django/forms/widgets/input.html'
    input_type = 'hidden'
    #template_name = 'django/forms/widgets/number.html'
    template_name = 'yaml_creator/widgets/FluxesInput.html'

    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def get_context(self, name, value, attrs):
        print('############# get_context value:')
        print(type(value))
        print(value)
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
        print('############# format value:')
        print(type(value))
        print(value)
        res=json.dumps(value)
        print(type(res))
        print(res)
        return res

    class Media:
        js=[ "yaml_creator/js/FluxFields.js", ]

