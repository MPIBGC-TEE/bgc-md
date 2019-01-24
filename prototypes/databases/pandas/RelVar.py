
import pandas as pd
from copy import copy,deepcopy
from testinfrastructure.helpers import pe
class RelVar:
    def __init__(self,valueConstraintDict:dict,record_constraints:list=[],rel_var_constraints:list=[]):
        ks=valueConstraintDict.keys()
        #make sure the keys are unique
        assert(len(ks)==len(set(ks)))
        self._valueConstraintDict=valueConstraintDict
        self._df=pd.DataFrame(columns=valueConstraintDict.keys())
        self._record_constraints=record_constraints
        self._rel_var_constraints=rel_var_constraints
        
    def check_value_constraints(self,record):
        rks=record.keys()
        #check the value constraints
        for k in rks:
            self._valueConstraintDict[k](record[k])

    def check_record_constraints(self,record):
        rks=record.keys()
        sks=self._valueConstraintDict.keys()
        #make sure that only the right keys are present
        assert(set(rks)==set(sks))
        # now call the checks in the list
        for func in self._record_constraints:
            func(record)

    def check_rel_var_constraints(self):
        for func in self._rel_var_constraints:
            func(self._df)

    def add_record(self,record:dict):
        self.check_value_constraints(record)
        self.check_record_constraints(record)

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
