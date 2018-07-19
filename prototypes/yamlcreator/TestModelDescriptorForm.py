from yaml_creator.forms import ModelDescriptorForm
data=dict()
data['pub_date']='2018-07-17'
data['doi']='http://google.com'
data['fluxes']='test'

mdf=ModelDescriptorForm(data)
mdf.data
mdf.is_valid()
mdf.cleaned_data
