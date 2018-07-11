from django import forms
from django.forms import ModelForm
from yaml_creator.models.ModelDescriptor import ModelDescriptor
from yaml_creator.fields import DOIField
from yaml_creator.fields import PUB_DATEField

class NameForm(forms.Form):
    your_name = forms.CharField(label='your name',max_length=100)

class ModelDescriptorForm(ModelForm):
    doi = DOIField(
	initial="http://doi.org/",
     	max_length=200,
        required=False,
        help_text='The dio of the original publication. It will be used to download bibliographic information including the abstract. If you provide this information yourself it will be used instead.', 
    )
    pub_date = PUB_DATEField()
    class Meta:
        model= ModelDescriptor
        fields=('doi','pub_date')
        help_texts={
            'pub_date': ('The date when this record was first created.'),
        }
    class Media:
        css={
            'all':(
                'admin/css/base.css',
                'admin/css/forms.css',
                  )
        }
        js=[
            "admin/js/core.js", # this is needed for the calendar
            #but somehow not mentioned int he widgets Media
        ]
