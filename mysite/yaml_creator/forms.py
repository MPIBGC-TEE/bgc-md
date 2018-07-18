from django.forms import Form,  ModelForm, CharField
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.fields import DOIField
from yaml_creator.fields import PUB_DATEField
from django.forms import URLField , DateField, CharField 

class NameForm(Form):
    your_url= URLField(label='your url',max_length=100)
    pub_date = DateField(
        help_text='The date when this record was first created.'
    )
class AdditionalVariableForm(Form):
    description=CharField(
        required=False,
        help_text='A short description of the variable.'
    )
    expression=CharField(
        required=False,
        help_text='sympy expression that relates the variable to others'
    )
    class Media:
        css={
            'all':(
                'admin/css/forms.css',
                'admin/css/base.css',
                'admin/css/widgets.css',
                  )
        }
        js=[
            "admin/js/core.js", # this is needed for the calendar
        ]


class StateVariableForm(Form):
    name=CharField(
        disabled=True,
        required=False,
        help_text='The name of the statevariable as used in the state vector'
    )
    description=CharField(
        required=False,
        help_text='A short description of the variable.'
    )

    #def __init__(self,*args,name,**kwargs):
    #    super().__init__(*args,**kwargs)
    #    self.name=name

    class Media:
        css={
            'all':(
                'admin/css/forms.css',
                'admin/css/base.css',
                'admin/css/widgets.css',
                  )
        }
        js=[
            "admin/js/core.js", # this is needed for the calendar
        ]

#class ModelDescriptorForm(ModelForm):
class ModelDescriptorForm(Form):
    #doi = DOIField(
    doi = URLField(
	initial="http://doi.org/",
     	max_length=200,
        #required=False,
        help_text='The dio of the original publication. It will be used to download bibliographic information including the abstract. If you provide this information yourself it will be used instead.', 
    )
    pub_date = PUB_DATEField(
    #pub_date = DateField(
        help_text='The date when this record was first created.'
    )

    statevector=CharField(
            help_text='Ordered list of state variables, e.g. C_1,C_2,C_3 , that form the state vector'
    )
    class Media:
        css={
            'all':(
                'admin/css/forms.css',
                'admin/css/base.css',
                'admin/css/widgets.css',
                  )
        }
        js=[
            "admin/js/core.js", # this is needed for the calendar
            #but somehow not mentioned in the widgets Media class
            #"admin/js/collapse.js", 
            #"admin/js/prepopulate.js", 
            #"admin/js/prepopulate_init.js", 
            #"admin/js/change_form.js", 
            #"admin/js/inlines.js", 
            #"admin/js/actions.js", 
            #"admin/js/urlify.js", 
        ]
