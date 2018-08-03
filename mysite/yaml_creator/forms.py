from django.forms import Form,  ModelForm, CharField, ChoiceField
from .models.ModelDescriptor import ModelDescriptor
from .models.FluxRepresentation import FluxRepresentation
from .models.Fluxes import Fluxes
from .models.Matrices import Matrices
from .fields import DOIField ,PUB_DATEField, FluxesField
from django.forms import URLField , DateField, CharField 

class NameForm(Form):
    your_url= URLField(label='your url',max_length=100)
    pub_date = DateField(
        help_text='The date when this record was first created.'
    )
class FluxRepresentationForm(Form):
    subClasses=FluxRepresentation.get_subclasses()
    subClassNames=[f.__name__ for f in subClasses]
    
    fluxrepresentation=ChoiceField(choices=[(name,name) for name in subClassNames])
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

class ModelDescriptorForm(Form):
    # Usually  a form is described by a static class definition.
    # This form is different from most predefined forms since it can actually
    # add fields dynamically depending on the data in the database or request.

    # E.g. Statevariable descriptions do not make sense if the statevector has not been defined yet (an hence the names of the statevariables are not known)
    # The fluxes field does not make sense if the component scheme is set to matrix...

    # There are various possibilities to deal with this situation. 
    # We could use different forms for parts of the model description 
    # or djangos formsets for repeated subforms.

    # There is however only ONE HTML form in our template 
    # (since we want ONE submit button for the form)
    # Therefore the most transparent solution is to reflect this fact on the
    # python side by one Form Class with a dynamic set of fields.\

    # Again there are different ways to achieve this 
    # (in decending order of power and copmplexity)
    # - MetaClasses
    #
    # - a Class factory function (using pythons type builting that returns 
    #   a tailormade class with the necessary fields added.
    #
    # - an overloaded __init__ method 
    #
    # We choose the simplest approach and define our own init method to 
    # listen to the data we recieve.
    # We use the fact that the fields are implemented as a dictionary
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        mycopy=dict()
        if len(args)>0:
            data=args[0]
            print("##########################################")
            print('data')
            mycopy.update(data)

        if "initial" in kwargs.keys():
            print('initial')
            initial=kwargs['initial']
            mycopy.update(initial)

            if 'statevector' in mycopy.keys():
                #sv.varliststring=mycopy["statevector"]
                subClasses=FluxRepresentation.get_subclasses()
                subClassNames=[f.__name__ for f in subClasses]
                field=ChoiceField(
                        choices=[(name,name) for name in subClassNames]
                        ,
                        required=False
                )
                self.fields['fluxrepresentation']= field
            
            #if 'fluxes' in data.keys():
            #    self.fields['fluxes']=FluxesField()
                
                



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
        ]
