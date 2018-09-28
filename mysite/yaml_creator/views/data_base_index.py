from yaml_creator.models.ModelDescriptor import ModelDescriptor,default_model_descriptor_folder_name
from django.shortcuts import render
from ..helpers import dataDirPath

def data_base_index(request):
    # at the moment we do not use the database
    # folder_names=[md.filename for
    #       ModelDescriptor.objects.order_by('-pub_date')]
    # but scan the datadirectory
    
    folder_names = [str(p.stem) for p in
                dataDirPath.iterdir()] if dataDirPath.exists() else []

    context={
        'folder_names':folder_names,
        'default_folder_name':default_model_descriptor_folder_name()}
    print('######################')
    print(context)
    print('######################')
    
    return render(request,'yaml_creator/data_base_index.html',context)
