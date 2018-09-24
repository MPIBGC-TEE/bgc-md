import re
from django.forms import Form,  ModelForm, CharField, ChoiceField
from .models.ModelDescriptor import ModelDescriptor
from .models.FluxRepresentation import FluxRepresentation
from .models.Fluxes import Fluxes
from .models.Matrices import Matrices
from .fields import DOIField ,PUB_DATEField, FluxesField
from django.forms import URLField , DateField, CharField 
from .helpers import var_names_from_state_vector_string



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
    # - MetaClasses
    #
    # - a Class factory function (using pythons type builtin that returns 
    #   a tailormade class with the necessary fields added.
    #
    # - an overloaded __init__ method 
    #
    # We choose the simplest approach and define our own init method to 
    # listen to the data we recieve.
    # We use the fact that the fields are implemented as a dictionary
    
    fluxRepKey='fluxrepresentation'
    stateVectorKey="statevector"
    
    stateVarKey="statevariable"
    stateVarNameKey=stateVarKey+"_name_"
    stateVarNamePattern=stateVarNameKey+'.*'
    stateVarDescKey=stateVarKey+"_description_"
    stateVarDescPattern=stateVarDescKey+'.*'
   

    # since Form uses a Django Metaclass that 
    # recognizes class variables that are instances of Field
    # we can just list the static fields here. They will
    # automatically end up in the internal fields property of every
    # instance.
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

#######################################################################
    fluxes= FluxesField(
        initial= {
                "names":["x","y","z"],
                "in_fluxes":[
                    {"target":"y","expression":"in "},
                    {"target":"z","expression":"in"}
                ],
                "internal_fluxes":[
                    {"source":"x", "target":"y","expression":"bla"},
                    {"source":"y", "target":"z","expression":"blub"}
                ],
                "out_fluxes":[
                    {"source":"x","expression":"out"},
                    {"source":"y","expression":"out"}
                ],
            }
        ,help_text="the target option will change when you change the source"
        ,required=False
        ) 

        # we have to adapt our init method since we want the set of fields to be displayed
    # depend on the data the instance is initialized with.
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        cls=self.__class__
        mycopy=dict()
        if len(args)>0:
            data=args[0]
            mycopy.update(data)

        if "initial" in kwargs.keys():
            print('initial')
            initial=kwargs['initial']
            mycopy.update(initial)

        d_keys=mycopy.keys()
        
        #stvNames=[ k.replace(cls.stateVarDescKey,"")  for k in d_keys if re.match(cls.stateVarDescPattern,k)]
        stvNames=cls.present_state_var_names(d_keys)
        #print("##########################################")
        #print('mycopy')
        #print(mycopy)
        #print('stvName')
        #print(stvNames)
        for name in stvNames:
            descField=CharField(
                required=False,
                help_text='A short description of the variable.',
                label="State variable {0} Description".format(name)
            )
            self.fields[cls.stateVarDescKey+name]= descField
           #if 'fluxes' in data.keys():
           #    self.fields['fluxes']=FluxesField()

        if cls.fluxRepKey in d_keys:
            subClassDict=FluxRepresentation.get_subclassDict()
            subClassNames=subClassDict.keys()
            field=ChoiceField(
                    choices=[(name,name) for name in subClassNames]
                    ,
                    required=False
            )
            self.fields[cls.fluxRepKey]= field
        
    
############################################# new (not overloaded) mothods    
    @ classmethod
    def descKey(cls,var_name):
        return cls.stateVarDescKey+var_name
    @classmethod
    def present_state_var_names(cls,keys):
        stvNames=[ k.replace(cls.stateVarDescKey,"")  for k in keys if re.match(cls.stateVarDescPattern,k)]
        return stvNames

    def extended_instance(self):
        cls=self.__class__
        cd=self.cleaned_data 
        # we add new key:initialValue pairs to the data dict
        # based on the data already available
        # The adaptive form class will add the required fields when it receives
        # this extended data dict
        ks=cd.keys()
    
        k=cls.stateVectorKey
        if k in ks:
            varliststring=cd[k]
            var_names=var_names_from_state_vector_string(varliststring)
            
            #now check which of the required fields for the statevariables are already
            #present
            pvn=cls.stateVarDescPattern
            stvNames=[ k.replace(cls.stateVarDescKey,"")  for k in ks if re.match(cls.stateVarDescPattern,k)]
            StateVector_var_name_set=set(var_names)
            present_var_name_set=set(stvNames)

            if StateVector_var_name_set!=present_var_name_set:
                # add description fields for all the variables 
                # present in the state vector
                for var_name in StateVector_var_name_set.difference(present_var_name_set):
                    cd.update({cls.descKey(var_name):None})
                
                # delete description fields for all the variables 
                # NOT present in the state vector
                for var_name in present_var_name_set.difference(StateVector_var_name_set):
                    cd.pop(cls.descKey(var_name))
            k=cls.fluxRepKey
            if not (k in ks):
                cd.update({k:None})

        # we return a new instance
        return cls(initial=cd),cd
