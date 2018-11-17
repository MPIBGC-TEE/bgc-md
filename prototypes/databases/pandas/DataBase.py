import pandas as pd
from copy import copy,deepcopy
from testinfrastructure.helpers import pe

class DataBase:
    def __init__(self,name:str,rel_var_dict:dict,constraints:list):
        self.name=name
        self._rel_var_dict=rel_var_dict
        self._constraints=constraints
    def add_rel_var(self,name,rel_var):
        newdb=deepcopy(self)
        newdb._rel_var_dict.update({name:rel_var})
        
    #def add_record(self,rel_var_name,record):
    #    rel_var=self._rel_var_dict[rel_var_name]
    #    new=rel_var.add_record()

    def check_constraints(self):
        # create the dictionary of dataframes since this is 
        # the agreed argument for the database checks
        df_dict={k:v._df for k,v in self._rel_var_dict.items()}
        for func in self._constraints:
            func(df_dict)

    def commit_transaction(self,actions:list):
        # the actions are list of triplets 
        new=deepcopy(self)
        for action in actions:
            rel_var_name,method_name,args=action
            rel_var=new._rel_var_dict[rel_var_name]
            #pe('( rel_var,method_name,args)',locals())
            pe('args',locals())
            pe('args[0:-2]',locals())
            
            method=getattr(rel_var,method_name)
            new._rel_var_dict[rel_var_name]=method(*args)
        new.check_constraints()
        return new
