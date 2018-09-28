from django.db import models
from django.utils import timezone
from pathlib import Path
import re
from ..config import dataDir,defaultYamlFileName

# Create your models here.
def default_model_descriptor_folder_name():
    #folder_names=[m.filename for m in ModelDescriptor.objects.all()]
    pd=Path(dataDir)
    if not pd.exists():
        pd.mkdir(parents=True)
    folder_names=[str(d.stem) for d in pd.iterdir() if d.is_dir]
    print('######################################## folder_names:')
    print(folder_names) 
    # set a default file name for a new yaml file that is not already present
    default_trunk='default_'
    num_str='[0-9]+'
    P_num=re.compile(num_str)
    P=re.compile(default_trunk+num_str)
    dl=[name for name in folder_names if P.match(name) is not None]
    print('######################################## dl:')
    print(dl)
    if len(dl)==0:
        yaml_file_name_default=default_trunk+'1'
    else:
        nmax=max([int(P_num.search(name).group()) for name in dl])
        yaml_file_name_default=default_trunk+str(nmax+1)

    return yaml_file_name_default
###############################################

class ModelDescriptor(models.Model):
    filename=models.CharField(max_length=200,primary_key=True,default=default_model_descriptor_folder_name)
    doi=models.URLField(max_length=200)
    #pub_date=models.DateTimeField('date published')
    pub_date=models.DateField('date published')

