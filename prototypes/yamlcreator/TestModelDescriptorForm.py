from yaml_creator.forms import ModelDescriptorForm
data=dict()
data['pub_date']='2018-07-17'
data['doi']='http://google.com'
data['statevector']='x1,x2'
#data['fluxrepresentation']='Matrices'

mdf=ModelDescriptorForm(data)
print(mdf.data)
print(mdf.is_valid())
mdf.cleaned_data
