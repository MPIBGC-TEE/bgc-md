import re
from django.forms import Form,  ModelForm, CharField, ChoiceField
from .models.ModelDescriptor import ModelDescriptor
from .models.FluxRepresentation import FluxRepresentation
from .models.Fluxes import Fluxes
from .models.Matrices import Matrices
from .fields import DOIField ,PUB_DATEField, FluxesField,StateVectorField
from django.forms import URLField , DateField, CharField 
from django.utils.html import conditional_escape #, html_safe
from django.utils.safestring import mark_safe
from datetime import datetime
from CompartmentalSystems.smooth_reservoir_model import SmoothReservoirModel
from testinfrastructure.helpers import pe,pp
import json
from sympy import sympify,Matrix



class ModelDescriptorForm(Form):
    error_css_class='error'
    required_css_class='required'
    # Usually  a form is described by a static class definition.
    # This form is different from predefined forms since it can actually
    # add fields dynamically depending on the data in the database or request.

    # E.g. Statevariable descriptions do not make sense if the statevector has not been defined yet 
    # (an hence the names of the statevariables are not known)
    # The fluxes field does not make sense if the component scheme is set to matrix...

    # There are various possibilities to deal with this situation. 
    # We could use different forms for parts of the model description 
    # or djangos formsets for repeated subforms.

    # There is however only ONE HTML form in our template 
    # (since we want only ONE submit button for the form)
    # Therefore the most transparent solution is to reflect this fact on the
    # python side by one Form Class with a dynamic set of fields.\

    # Again there are different ways to achieve this 
    # We choose the simplest approach and define our own init method to 
    # listen to the data we recieve.
    # We use the fact that the fields are implemented as a dictionary
    fluxesKey='fluxes'
    fluxRepKey='fluxrepresentation'
    stateVectorKey="statevector"
    timeSymbolKey="timesymbol"
    
    #stateVarNameKey=stateVarKey+"_name_"
    #stateVarNamePattern=stateVarNameKey+'.*'
    stateVarKey="statevariable"
    stateVarDescPrefix=stateVarKey+"_description_"
    stateVarDescPattern=stateVarDescPrefix+'.*'

    additionalVarKey="additional_variable"
    additionalVarDescPrefix=additionalVarKey+"_description_"
    additionalVarDescPattern=additionalVarDescPrefix+'.*'

    funcKey="function"
    funcDescPrefix=funcKey+"_description_"
    funcDescPattern=funcDescPrefix+'.*'
   

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
	    initial=datetime.now(),
        help_text='The date when this record was first created.'
    )

    statevector=StateVectorField(
            help_text='Ordered, comma separated  list of state variables, e.g. C_1,C_2,C_3 , that form the state vector.'
    )
    timesymbol=CharField(
            initial="t",
            help_text='the symbol used to represent time'

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
    # we have to adapt our init method since we want the set of fields to be displayed
    # to depend on the data the instance is initialized with.
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
        
        #stvNames=[ k.replace(cls.stateVarDescPrefix,"")  for k in d_keys if re.match(cls.stateVarDescPattern,k)]
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
            self.fields[cls.stateVarDescPrefix+name]= descField

        if cls.fluxRepKey in d_keys:
            subClassDict=FluxRepresentation.get_subclassDict()
            subClassNames=subClassDict.keys()
            field=ChoiceField(
                    choices=[(name,name) for name in subClassNames]
                    ,
                    required=False
            )
            self.fields[cls.fluxRepKey]= field
            self.fields[cls.fluxesKey]= FluxesField(
                initial={
                    "names":stvNames
                    ,
                    "in_fluxes":[]
                    ,
                    "internal_fluxes":[]
                    ,
                    "out_fluxes":[]
                }
                # example structure
                #initial={
                #    "names":['x','y','z']
                #    ,
                #    "in_fluxes":[
                #        {"target":"y","expression":"x**3"}
                #       #,{"target":"z","expression":"y**3"}
                #    ]
                #    ,
                #    "internal_fluxes":[
                #        {"source":"x", "target":"y","expression":"x**3"}
                #        # ,{"source":"y", "target":"z","expression":"y**3"}
                #    ]
                #    ,
                #    "out_fluxes":[
                #        {"source":"x","expression":"x"}
                #       #,{"source":"y","expression":"y"}
                #    ]
                #}
                ,help_text="the target option will change when you change the source"
                ,required=False
                ) 

        for name in cls.present_additional_var_names(d_keys):
            descField=CharField(
                required=False,
                help_text='A short description of the variable.',
                label="{0} Description".format(name)
            )
            self.fields[cls.additionalVarDescPrefix+name]= descField

        for name in cls.present_func_names(d_keys):
            descField=CharField(
                required=False,
                help_text='A short description of the function.',
                label="{0} Description".format(name)
            )
            self.fields[cls.funcDescPrefix+name+'(...)']= descField

    
        
    
############################################# new (not overloaded) mothods    
    @ classmethod
    def descKey(cls,var_name):
        return cls.stateVarDescPrefix+var_name
    @classmethod
    def present_state_var_names(cls,keys):
        stvNames=[ k.replace(cls.stateVarDescPrefix,"")  for k in keys if re.match(cls.stateVarDescPattern,k)]
        return stvNames

    @ classmethod
    def additionalVarDescKey(cls,var_name):
        field_name=cls.additionalVarDescPrefix+var_name
        return field_name

    @classmethod
    def present_additional_var_names(cls,keys):
        Names=[ k.replace(cls.additionalVarDescPrefix,"")  for k in keys if re.match(cls.additionalVarDescPattern,k)]
        return Names
    
    @ classmethod
    def funcDescKey(cls,var_name):
        field_name=cls.funcDescPrefix+var_name
        return field_name

    @classmethod
    def present_func_names(cls,keys):
        Names=[ k.replace(cls.funcDescPrefix,"")  for k in keys if re.match(cls.funcDescPattern,k)]
        return Names

    @classmethod
    def update_state_var_keys(cls,cd):
        ks=cd.keys()
        k=cls.stateVectorKey
        if k in ks:
            #varliststring=cd[k]
            #var_names=var_names_from_state_vector_string(varliststring)
            var_names=[n for n in map(str,sympify(cd[k]))]
            
            #now check which of the required description fields for the statevariables are already
            #present
            pvn=cls.stateVarDescPattern
            stvNames=[ k.replace(cls.stateVarDescPrefix,"")  for k in ks if re.match(cls.stateVarDescPattern,k)]
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
        return(cd)


    @classmethod
    def update_external_func_keys(cls,cd):
        pe('cd',locals())
        rm=cls.srm(cd)
        # find the yet additional variables to

        fs=rm.function_expressions
        func_names=[fn for fn in map(lambda f:str(type(f)),fs)]

        ks=cd.keys()
        pfn=cls.present_func_names(ks)
        
        if pfn!=func_names:
            # add description fields for all additiona variables 
            # present in any expression
            for var_name in set(func_names).difference(pfn):
                cd.update({cls.funcDescKey(var_name):None})
            

            # delete description fields for all the variables 
            # NOT present in any expression
            del_names=set(pfn).difference(func_names)
            for var_name in del_names :
                cd.pop(cls.funcDescKey(var_name))
        return cd

    
    @classmethod
    def srm(cls,cd):
        fluxes=cd[cls.fluxesKey]
        varliststring=cd[cls.stateVectorKey]
        pe('type(fluxes)',locals())
        names=fluxes["names"]
        outF=fluxes["out_fluxes"]
        intF=fluxes["internal_fluxes"]
        state_var_tupel=sympify(varliststring)

        time_symbol=sympify(cd[cls.timeSymbolKey])
        
        inSym={sympify(flux['target']):sympify(flux['expression']) for flux in fluxes["in_fluxes"]}
        outSym={sympify(flux['source']):sympify(flux['expression']) for flux in fluxes["out_fluxes"]}
        internalSym={(sympify(flux['source']),sympify(flux['target'])):sympify(flux['expression']) for flux in fluxes["internal_fluxes"]}

        rm = SmoothReservoirModel.from_state_variable_indexed_fluxes(list(state_var_tupel), time_symbol, inSym, outSym, internalSym)
        return(rm)


    @classmethod
    def update_additional_var_keys(cls,cd):
        rm=cls.srm(cd)
        # find the yet additional variables to
        fs=rm.free_symbols
        state_var_tupel=tuple(rm.state_vector)
        additional=fs.difference(state_var_tupel).difference([rm.time_symbol])
        additional_names=[n for n in map(str,additional)]
        pe('additional_names',locals())
        
        ks=cd.keys()
        pavn=cls.present_additional_var_names(ks)
        pe('pavn',locals())
        
        if pavn!=additional_names:
            # add description fields for all additiona variables 
            # present in any expression
            for var_name in set(additional_names).difference(pavn):
                cd.update({cls.additionalVarDescKey(var_name):None})
            

            # delete description fields for all the variables 
            # NOT present in any expression
            del_names=set(pavn).difference(additional_names)
            pe('del_names',locals())
            for var_name in del_names :
                cd.pop(cls.additionalVarDescKey(var_name))
        return cd

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
            cd=cls.update_state_var_keys(cd) 
            #varliststring=cd[k]

            k=cls.fluxRepKey
            if not (k in ks):
                cd.update({k:None})

            if cls.fluxesKey in ks:
                cd=cls.update_external_func_keys(cd)
                cd=cls.update_additional_var_keys(cd)

        # we return a new instance
        return cls(initial=cd),cd

    def _html_output(self, normal_row, error_row, row_ender, help_text_html, errors_on_separate_row):
        "Output HTML. Used by as_table(), as_ul(), as_p()."
        top_errors = self.non_field_errors()  # Errors that should be displayed above all fields.
        output, hidden_fields = [], []
        def per_field():
            html_class_attr = ''
            bf = self[name]
            bf_errors = self.error_class(bf.errors)
            if bf.is_hidden:
                if bf_errors:
                    top_errors.extend(
                        [_('(Hidden field %(name)s) %(error)s') % {'name': name, 'error': str(e)}
                         for e in bf_errors])
                hidden_fields.append(str(bf))
            else:
                # Create a 'class="..."' attribute if the row should have any
                # CSS classes applied.
                css_classes = bf.css_classes()
                if css_classes:
                    html_class_attr = ' class="%s"' % css_classes

                if errors_on_separate_row and bf_errors:
                    output.append(error_row % str(bf_errors))

                if bf.label:
                    label = conditional_escape(bf.label)
                    label = bf.label_tag(label) or ''
                else:
                    label = ''

                if field.help_text:
                    help_text = help_text_html % field.help_text
                else:
                    help_text = ''

                output.append(normal_row % {
                    'errors': bf_errors,
                    'label': label,
                    'field': bf,
                    'help_text': help_text,
                    'html_class_attr': html_class_attr,
                    'css_classes': css_classes,
                    'field_name': bf.html_name,
                })
        for name, field in self.fields.items():
            per_field()


        if top_errors:
            output.insert(0, error_row % top_errors)

        if hidden_fields:  # Insert any hidden fields in the last row.
            str_hidden = ''.join(hidden_fields)
            if output:
                last_row = output[-1]
                # Chop off the trailing row_ender (e.g. '</td></tr>') and
                # insert the hidden fields.
                if not last_row.endswith(row_ender):
                    # This can happen in the as_p() case (and possibly others
                    # that users write): if there are only top errors, we may
                    # not be able to conscript the last row for our purposes,
                    # so insert a new, empty row.
                    last_row = (normal_row % {
                        'errors': '',
                        'label': '',
                        'field': '',
                        'help_text': '',
                        'html_class_attr': html_class_attr,
                        'css_classes': '',
                        'field_name': '',
                    })
                    output.append(last_row)
                output[-1] = last_row[:-len(row_ender)] + str_hidden + row_ender
            else:
                # If there aren't any rows in the output, just append the
                # hidden fields.
                output.append(str_hidden)
        return mark_safe('\n'.join(output))
