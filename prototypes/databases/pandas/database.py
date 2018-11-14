import pandas as pd
import numpy as np
from copy import copy,deepcopy
from sympy import sympify,Matrix
from testinfrastructure.helpers import pe
class DataBase:
    def __init__(self,name,rel_var_dict,constraints:list):
        self.name=name
        self._rel_var_dict=rel_var_dict
    def add_rel_var(self,name,rel_var):
        newdb=deepcopy(self)
        newdb._rel_var_dict.update({name:rel_var})
        
    def add_record(self,rel_var_name,record):
        rel_var=self._rel_var_dict[rel_var_name]

    def check_constraints(self):
        df_dict={k:val._df for k,v in self.rel_var_dict.items()}
        for func in constraints:
            func(df_dict)

    

class RelVar:
    def __init__(self,valueConstraintDict:dict,record_constraints:list=[],rel_var_constraints:list=[]):
        ks=valueConstraintDict.keys()
        #make sure the keys are unique
        assert(len(ks)==len(set(ks)))
        self._valueConstraintDict=valueConstraintDict
        self._df=pd.DataFrame(columns=valueConstraintDict.keys())
        self._record_constraints=record_constraints
        self._rel_var_constraints=rel_var_constraints
        
    def check_rel_var_constraints(self):
        for func in self._rel_var_constraints:
            func(self._df)

    def add_record(self,record:dict):
        rks=record.keys()
        sks=self._valueConstraintDict.keys()
        
        #make sure that only the right keys are present
        assert(set(rks)==set(sks))
        
        #check the value constraints
        for k in rks:
            self._valueConstraintDict[k](record[k])

        # pandas wants lists or arrays as values therefore we wrap
        listrecord={k:[v] for k,v in record.items()}
        NRV=deepcopy(self)
        # only add a new line if the new record is not allready contained in the dataframe
        new_line=pd.DataFrame(listrecord)
        df=NRV._df
        dicts=[dict(df.iloc[i]) for i in range(len(df))]
        if len(df)==0 or not listrecord in dicts:
            NRV._df=self._df.append(new_line)
            #print('NRV._df')
            #print(NRV._df)

        NRV.check_rel_var_constraints()
        return NRV
    
        #self.models=pd.dataframe(



#per cell constraints
def isString(x):
    assert(type(x)==str)

def yieldsMatrix(x):
    isString(x)
    assert(type(sympify(x))==Matrix)

def yieldsVector(x):
    yieldsMatrix(x)
    assert((sympify(x)).shape[1]==1)


def isFluxRep(x):
    assert(type(x)==str)
    assert(x=='Fluxes'or x=="Matrices")

#per record constraints
def matrixDimensionsAgree(record):
    B=sympify(record['matrix_expression'])
    I=sympify(record['input_vector_expression'])
    assert(I.cols==1)
    assert(I.rows==B.rows)
    
#per relvar constraints
def make_key_checker(col_name_set):
    def is_key(df):
        # the function assumes to be called with a dataframe 
        #(which is the internal representation of the relvar)
        assert(set(df).issuperset(col_name_set))
        subframe=df[list(col_name_set)]
        pe('subframe',locals())
        #create a tuple list 
        tuples=[tuple(subframe.iloc[i]) for i in range(len(subframe))]
        assert(len(tuples)==len(pd.unique(tuples)))
    return is_key
   

    

def eitherFluxOrMatrix(df_dict):
    # the function assumes to be called with a dictionary of dataframes
    matrix_model_ids=set(df_dict['CompartmentalMatricesAndInputVectors']['model_id'])
    assert(set(df_dict['InFluxes']['model_id']).isdisjoint(matrix_model_ids))
    assert(set(df_dict['OutFluxes']['model_id']).isdisjoint(matrix_model_ids))
    assert(set(df_dict['InternalFluxes']['model_id']).isdisjoint(matrix_model_ids))

   


#create Tables
Models=RelVar(
        {"folder_name":isString,"name":isString},
        record_constraints=None,
        rel_var_constraints=[make_key_checker(set({'folder_name'}))]
)
Variables=RelVar(
        {"symbol":isString,"id":isString,"description":isString},
        record_constraints=None,
        rel_var_constraints=[make_key_checker(set({'id','symbol'}))]
)
InFluxes=RelVar({"targetVariable_symbol":isString,"model_id":isString,"expression":isString})
OutFluxes=RelVar({"sourceVariable_symbol":isString,"model_id":isString,"expression":isString})
InternalFluxes=RelVar({"sourceVariable_symbol":isString,"targetVariable_symbol":isString,"model_id":isString,"expression":isString})
CompartmentalMatricesAndInputVectors=RelVar({"compartmental_matrix_expression":yieldsMatrix,"input_vector_expression":yieldsVector,"model_id":isString})

#per database constraints
def variablesReferToExistingModels(df_dict):
    # this is a classic foreign key constraint
    mt=df_dict['Models']
    vt=df_dict['Variables']
    assert((set(Variables._df['id'])).issubset(set(Models._df['folder_name'])))


db1=DataBase(
    'ModelDataBase',
    {
        'Models':Models,
        'Variables':Variables,
        'InFluxes':InFluxes,
        'OutFluxes':OutFluxes,
        'InternalFluxes':InternalFluxes,
        'CompartmentalMatricesAndInputVectors':CompartmentalMatricesAndInputVectors
        }[eitherFluxOrMatrix])

#insert data
Models=Models.add_record({'folder_name':'default_1','name':"mmtest"})
#Models=Models.add_record({'folder_name':'default_1','name':"mmtest2"})
Variables=Variables.add_record({'symbol':'x','id':"default_1",'description':''})
Variables=Variables.add_record({'symbol':'y','id':"default_1",'description':''})
Variables=Variables.add_record({'symbol':'z','id':"default_1",'description':''})
#Variables=Variables.add_record({'symbol':'z','id':"default_1",'description':''})
#
InFluxes=InFluxes.add_record( {
    'targetVariable_symbol':'x', 'model_id':'default_1', 'expression':'1'
})
InFluxes=InFluxes.add_record( {
    'targetVariable_symbol':'y', 'model_id':'default_1', 'expression':'2'
})
OutFluxes=OutFluxes.add_record( {
    'sourceVariable_symbol':'x', 'model_id':'default_1', 'expression':'x**1'
})
OutFluxes=OutFluxes.add_record( {
    'sourceVariable_symbol':'y', 'model_id':'default_1', 'expression':'x**1'
})
InternalFluxes=InternalFluxes.add_record( {
    'sourceVariable_symbol':'x','targetVariable_symbol':'y', 'model_id':'default_1', 'expression':'x**1'
})
InternalFluxes=InternalFluxes.add_record( {
    'sourceVariable_symbol':'y','targetVariable_symbol':'x', 'model_id':'default_1', 'expression':'x**1'
})
#CompartmentalMatricesAndInputVectors=CompartmentalMatricesAndInputVectors.add_record( {
#    'compartmental_matrix_expression':'Matrix([[1,1],[1,1]])','input_vector_expression':'Matrix([x,y])', 'model_id':'default_1'
#})
#
