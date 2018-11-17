from .config import dataDir
from pathlib import Path
from django.db import transaction
from .models.Variable import Variable
from .models.ModelDescriptor import ModelDescriptor
from .models.StateVectorPosition import StateVectorPosition 
dataDirPath=Path(dataDir)


@transaction.atomic
def storeModel(folder_name:str,variable_list:list):
    m=ModelDescriptor(folder_name=folder_name)
    m.save()
    for i,v in enumerate(variable_list): 
        v=Variable(model_id=m,symbol=v)
        v.save()
        p=StateVectorPosition(var_id=v,pos_id=i)
        p.save()
