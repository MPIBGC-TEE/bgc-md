from yaml_creator.models import ModelDescriptor
from django.shortcuts import render

def data_base_index(request):
    latest_modeldescriptor_list = ModelDescriptor.objects.order_by('-pub_date')
    context={
        'latest_modeldescriptor_list':latest_modeldescriptor_list,
        'yaml_file_name_default':'default_34'}
    print('######################')
    print(latest_modeldescriptor_list)
    print('######################')
    
    return render(request,'yaml_creator/data_base_index.html',context)
