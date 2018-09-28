from .config import dataDir
from pathlib import Path
dataDirPath=Path(dataDir)
from django.core.exceptions import ValidationError
def var_names_from_state_vector_string(varliststring):
    var_names_list=varliststring.split(',')
    var_names_set=set(var_names_list)
    if len(var_names_list)!=len(var_names_set):
        raise ValidationError(
            Template("The vartiable names in the  string representation of the statevector were not unique").substitute(v=varliststring)
            )
    return var_names_list  

