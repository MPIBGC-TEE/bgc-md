import pandas as pd
import numpy as np
from copy import copy
class DataBase:
    def __init__(self,name,constraints:list):
        self.name=name
    

class RelVar:
    def __init__(self,valueConstraintDict:dict,data_base:DataBase):
        ks=valueConstraintDict.keys()
        #make sure the keys are unique
        assert(len(ks)==len(set(ks)))
        self._valueConstraintDict=valueConstraintDict
        self._db=data_base
        self._df=pd.DataFrame(columns=valueConstraintDict.keys())


    def add_record(self,record:dict):
        rks=record.keys()
        sks=self._valueConstraintDict.keys()
        #make sure that only the right keys are present
        #print(rks)
        #print(sks)
        assert(set(rks)==set(sks))
        #check the value constraints
        for k in rks:
            self._valueConstraintDict[k](record[k])

        # pandas wants lists or arrays as values therefore we wrap
        listrecord={k:[v] for k,v in record.items()}
        NRV=copy(self)
        NRV._df=self._df.append(pd.DataFrame(listrecord))
        return NRV
    
        #self.models=pd.dataframe(
def eitherFluxOrMatrix(df_dict):
    # the function assumes to be called with a dictionary of dataframes
    mt=df_dict['Models']
    vt=df_dict['Variables']
    #

db1=DataBase('ModelDataBase',[eitherFluxOrMatrix])



def isString(x):
    assert(type(x)==str)

def isFluxRep(x):
    assert(type(x)==str)
    assert(x=='Fluxes'or x=="Matrices")

Models=RelVar({"folder_name":isString,"name":isString,"flux_representation":isFluxRep},db1)
Models=Models.add_record({'folder_name':'default_1','name':"mmtest",'flux_representation':'Fluxes'})

InFluxes=RelVar({"targetVariable_symbol":isString,"targetVariable_model_id":isString,"expression":isString},db1)
InFluxes=InFluxes.add_record( {
    'targetVariable_symbol':'x', 'targetVariable_model_id':'default_1', 'expression':'x**1'
})
InFluxes=InFluxes.add_record( {
    'targetVariable_symbol':'y', 'targetVariable_model_id':'default_1', 'expression':'x**1'
})
