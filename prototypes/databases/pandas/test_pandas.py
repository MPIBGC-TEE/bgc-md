import unittest
import pandas as pd
import numpy as np
from copy import copy,deepcopy
from sympy import sympify,Matrix
from testinfrastructure.helpers import pe
from DataBase import DataBase
from RelVar import RelVar

#per cell constraints
def isString(x):
    assert(type(x)==str)

def yieldsMatrix(x):
    isString(x)
    assert(type(sympify(x))==Matrix)

def yieldsVector(x):
    yieldsMatrix(x)
    assert((sympify(x)).shape[1]==1)


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
   
class TestModelDataBase(unittest.TestCase):
    def test_transaction(self):
        
        #create Tables
        Models=RelVar(
                {"folder_name":isString,"name":isString},
                rel_var_constraints=[make_key_checker(set({'folder_name'}))]
        )
        Variables=RelVar(
                {"symbol":isString,"id":isString,"description":isString},
                record_constraints=[],
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
        
        def eitherFluxOrMatrix(df_dict):
            # the function assumes to be called with a dictionary of dataframes
            matrix_model_ids=set(df_dict['CompartmentalMatricesAndInputVectors']['model_id'])
            assert(set(df_dict['InFluxes']['model_id']).isdisjoint(matrix_model_ids))
            assert(set(df_dict['OutFluxes']['model_id']).isdisjoint(matrix_model_ids))
            assert(set(df_dict['InternalFluxes']['model_id']).isdisjoint(matrix_model_ids))
        
           
        
        db1=DataBase(
            'ModelDataBase',
            {
                'Models':Models,
                'Variables':Variables,
                'InFluxes':InFluxes,
                'OutFluxes':OutFluxes,
                'InternalFluxes':InternalFluxes,
                'CompartmentalMatricesAndInputVectors':CompartmentalMatricesAndInputVectors
            },
            [
                eitherFluxOrMatrix,
                variablesReferToExistingModels
                
            ]
        )
        
        
        # define some example transactions
        # add a Model instance 
        db1=db1.commit_transaction(
                [
                    (
                        'Models',
                        'add_record',
                        ({'folder_name':'default_1','name':'mm_test1'},)
                    )
                ]
        )
    @unittest.skip('not implemented yet')
    def test_add_RelVar(self):
        pass

    
