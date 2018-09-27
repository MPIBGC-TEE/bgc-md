from yaml_creator.models.ModelDescriptor import ModelDescriptor,default_model_descriptor_folder_name
from django.shortcuts import render

def data_base_index(request):
    latest_modeldescriptor_list = ModelDescriptor.objects.order_by('-pub_date')
    context={
        'latest_modeldescriptor_list':latest_modeldescriptor_list,
        'yaml_file_name_default':default_model_descriptor_folder_name()}
    print('######################')
    print(context)
    print('######################')
    
    return render(request,'yaml_creator/data_base_index.html',context)
